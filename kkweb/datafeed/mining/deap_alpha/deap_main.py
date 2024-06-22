import copy

from deap_patch import *  # noqa
from deap import base, creator, gp
from deap import tools
from datafeed.mining.deap_alpha.add_ops import *
from datafeed.dataloader import CSVDataloader
from config import DATA_DIR_QUOTES
import pandas as pd
from loguru import logger


def convert_inverse_prim(prim, args):
    """
    Convert inverse prims according to:
    [Dd]iv(a,b) -> Mul[a, 1/b]
    [Ss]ub(a,b) -> Add[a, -b]
    We achieve this by overwriting the corresponding format method of the sub and div prim.
    """
    prim = copy.copy(prim)

    converter = {
        'Add': lambda *args_: "{}+{}".format(*args_),
        'Mul': lambda *args_: "{}*{}".format(*args_),
        'fsub': lambda *args_: "{}-{}".format(*args_),
        'fdiv': lambda *args_: "{}/{}".format(*args_),
        'fmul': lambda *args_: "{}*{}".format(*args_),
        'fadd': lambda *args_: "{}+{}".format(*args_),
        # 'fmax': lambda *args_: "max_({},{})".format(*args_),
        # 'fmin': lambda *args_: "min_({},{})".format(*args_),

        'isub': lambda *args_: "{}-{}".format(*args_),
        'idiv': lambda *args_: "{}/{}".format(*args_),
        'imul': lambda *args_: "{}*{}".format(*args_),
        'iadd': lambda *args_: "{}+{}".format(*args_),
        # 'imax': lambda *args_: "max_({},{})".format(*args_),
        # 'imin': lambda *args_: "min_({},{})".format(*args_),
    }

    prim_formatter = converter.get(prim.name, prim.format)

    return prim_formatter(*args)


def stringify_for_sympy(f):
    """Return the expression in a human readable string.
    """
    string = ""
    stack = []
    for node in f:
        stack.append((node, []))
        while len(stack[-1][1]) == stack[-1][0].arity:
            prim, args = stack.pop()
            string = convert_inverse_prim(prim, args)
            if len(stack) == 0:
                break  # If stack is empty, all nodes should have been seen
            stack[-1][1].append(string)
    # print(string)
    return string


def calc_ic(x, y):
    """个体fitness函数"""
    ic = pd.Series(x.corr(y))
    return ic


def map_exprs(evaluate, invalid_ind, gen, label, split_date):
    names, features = [], []
    for i, expr in enumerate(invalid_ind):
        names.append(f'GP_{i:04d}')
        features.append(stringify_for_sympy(expr))

    features = [f.lower() for f in features]
    # for name, feature in zip(names, features):
    #    print(name, ':', feature)

    all_names = names.copy()
    all_names.append(label)
    all_features = features.copy()
    all_features.append('label(close,5)')

    df = CSVDataloader(path=DATA_DIR_QUOTES.resolve(), symbols=['510300.SH', '510880.SH', '159915.SZ']).load(
        all_features, all_names)
    df.set_index([df['symbol'], df.index], inplace=True)
    # df.dropna(inplace=True)

    # 将IC划分成训练集与测试集
    df_train = df[df.index.get_level_values(1) < split_date]
    df_valid = df[df.index.get_level_values(1) >= split_date]
    # print(df_train)
    # print(names, features)

    ic_train = df_train[names].groupby(level=0, group_keys=False).agg(lambda x: calc_ic(x, df_train[label])).mean()
    ic_valid = df_valid[names].groupby(level=0, group_keys=False).agg(lambda x: calc_ic(x, df_valid[label])).mean()
    # print('ic_train', ic_train)
    # print('ic_valid', ic_valid)

    results = {}
    for name, factor in zip(names, features):
        results[factor] = {'ic_train': ic_train.loc[name],
                           'ic_valid': ic_valid.loc[name],
                           }
    # print(results)
    return [(v['ic_train'], v['ic_valid']) for v in results.values()]


def init_pset():
    pset = gp.PrimitiveSetTyped("MAIN", [], RET_TYPE)
    pset = add_constants(pset)
    pset = add_operators(pset)
    pset = add_factors(pset)
    return pset


def init_creator():
    # 可支持多目标优化
    # TODO 必须元组，1表示找最大值,-1表示找最小值
    FITNESS_WEIGHTS = (1.0, 1.0)
    creator.create("FitnessMulti", base.Fitness, weights=FITNESS_WEIGHTS)
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti)
    return creator


def init_toolbox(creator):
    toolbox = base.Toolbox()
    pset = init_pset()
    toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=2, max_=5)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", print)  # 不单独做评估了，在map中一并做了

    toolbox.register("select", tools.selTournament, tournsize=3)  # 目标优化
    # toolbox.register("select", tools.selNSGA2)  # 多目标优化 FITNESS_WEIGHTS = (1.0, 1.0)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    import operator
    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

    from datetime import datetime
    dt1 = datetime(2021, 1, 1)
    LABEL_y = 'return_5'
    from itertools import count
    toolbox.register('map', map_exprs, gen=count(), label=LABEL_y, split_date=dt1)

    return toolbox


if __name__ == '__main__':
    import warnings

    warnings.filterwarnings('ignore', category=RuntimeWarning)

    logger.info('开始Deap因子挖掘...')
    random.seed(9527)
    creator = init_creator()
    toolbox = init_toolbox(creator)
    n = 100
    pop = toolbox.population(n=n)
    logger.info('完成初代种群初始化：{}个'.format(n))
    hof = tools.HallOfFame(10)

    # 只统计一个指标更清晰
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # 打补丁后，名人堂可以用nan了，如果全nan会报警
    stats.register("avg", np.nanmean, axis=0)
    stats.register("std", np.nanstd, axis=0)
    stats.register("min", np.nanmin, axis=0)
    stats.register("max", np.nanmax, axis=0)

    # 使用修改版的eaMuPlusLambda
    population, logbook = eaMuPlusLambda(pop, toolbox,
                                         # 选多少个做为下一代，每次生成多少新个体
                                         mu=150, lambda_=100,
                                         # 交叉率、变异率，代数
                                         cxpb=0.5, mutpb=0.1, ngen=2,
                                         # 名人堂参数
                                         # alpha=0.05, beta=10, gamma=0.25, rho=0.9,
                                         stats=stats, halloffame=hof, verbose=True,
                                         # 早停
                                         early_stopping_rounds=5)

    print('=' * 60)
    print(logbook)

    print('=' * 60)


    def print_population(population):

        for p in population:
            expr = stringify_for_sympy(p)
            print(expr, p.fitness)


    print_population(hof)
