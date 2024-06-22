# TODO: 请在此文件中添加算子和因子
# TODO: 由于部分算子计算过慢，这里临时屏蔽了
import random


class RET_TYPE:
    # 是什么不重要
    # 只要addPrimitive中in_types, ret_type 与 PrimitiveSetTyped("MAIN", [], ret_type)中
    # 这三种type对应即可
    pass


# 改个名，因为从polars_ta中默认提取的annotation是Expr
# TODO 如果用使用其它库，这里可能要修改
Expr = RET_TYPE


def _random_int_():
    return random.choice([1, 3, 5, 10, 20, 40, 60])


def add_constants(pset):
    """添加常量"""
    # !!! 名字一定不能与其它名字重，上次与int一样，结果其它地方报错 [<class 'deap.gp.random_int'>]
    pset.addEphemeralConstant('_random_int_', _random_int_, int)
    return pset


def add_operators_base(pset):
    """基础算子"""
    # 无法给一个算子定义多种类型，只好定义多个不同名算子，之后通过helper.py中的convert_inverse_prim修正
    pset.addPrimitive(dummy, [Expr, Expr], Expr, name='fadd')
    pset.addPrimitive(dummy, [Expr, Expr], Expr, name='fsub')
    pset.addPrimitive(dummy, [Expr, Expr], Expr, name='fmul')
    pset.addPrimitive(dummy, [Expr, Expr], Expr, name='fdiv')
    # pset.addPrimitive(dummy, [Expr, Expr], Expr, name='fmax')
    # pset.addPrimitive(dummy, [Expr, Expr], Expr, name='fmin')

    pset.addPrimitive(dummy, [Expr, int], Expr, name='iadd')
    pset.addPrimitive(dummy, [Expr, int], Expr, name='isub')
    pset.addPrimitive(dummy, [Expr, int], Expr, name='imul')
    pset.addPrimitive(dummy, [Expr, int], Expr, name='idiv')

    return pset


def add_unary_ops(pset):
    from datafeed.expr_functions import unary_funcs
    for func in unary_funcs:
        pset.addPrimitive(dummy, [Expr], Expr, name=func)


def add_unary_rolling_ops(pset):
    from datafeed.expr_functions import unary_rolling_funcs
    for func in unary_rolling_funcs:
        pset.addPrimitive(dummy, [Expr, int], Expr, name=func)


def add_binary_ops(pset):
    from datafeed.expr_functions import binary_funcs
    for func in binary_funcs:
        pset.addPrimitive(dummy, [Expr, Expr], Expr, name=func)


def add_binary_rolling_ops(pset):
    from datafeed.expr_functions import binary_roilling_funcs
    for func in binary_roilling_funcs:
        pset.addPrimitive(dummy, [Expr, Expr, int], Expr, name=func)


def add_operators(pset):
    """添加算子"""
    pset = add_operators_base(pset)
    add_unary_ops(pset)
    add_binary_ops(pset)
    add_unary_rolling_ops(pset)
    ##add_binary_rolling_ops(pset)

    return pset


def add_factors(pset):
    pset.addTerminal(1, Expr, name='OPEN')
    pset.addTerminal(1, Expr, name='HIGH')
    pset.addTerminal(1, Expr, name='LOW')
    pset.addTerminal(1, Expr, name='CLOSE')
    pset.addTerminal(1, Expr, name='VOLUME')
    # pset.addTerminal(1, Expr, name='AMOUNT')

    return pset


def dummy(*args):
    # 由于生成后的表达计算已经被map和evaluate接管，所以这里并没有用到，可随便定义
    print('dummy')
    return 1
