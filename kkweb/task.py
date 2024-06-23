import importlib
from dataclasses import dataclass, field, asdict

import bt.algos

import algos_extend
import config
from config import DATA_DIR
# from kkdatac.dataloader import CSVDataloader
import json, uuid


@dataclass
class Task:
    _id: str = None
    name: str = "策略名称"
    desc: str = ""

    # 标的池
    symbols: list[str] = field(default_factory=list)

    algo_period: str = "RunDaily"
    algo_period_days: int = 20  # 仅当RunDays时需要

    # 规则选标的：当rules_buy或rules_sell至少有一条规则时，添加SelectBySignal算子， 在SelectAll之后
    rules_buy: list[str] = field(default_factory=list)  # roc(close,20)>0.08
    at_least_buy: int = 1
    rules_sell: list[str] = field(default_factory=list)  # roc(close,20)<0
    at_least_sell: int = 1

    # 排序算子： 当order_by不为空时，在选股之后，添加SelectTopK算子
    order_by: str = ""  # 比如roc(close,20)，或者 roc(close,20)+ slope(close,20)
    topK: int = 1
    dropN: int = 0
    b_ascending: bool = 0  # 默认降序, 0=False

    # 仓位分配，默认等权
    algo_weight: str = "WeighEqually"
    algo_weight_fix: list = field(default_factory=list)  # 当WeightFix时需要

    feature_names: list = field(default_factory=list)  # roc(close,20)
    features: list = field(default_factory=list)  # roc_20

    # 回测时用户可以改变的，不变就使用默认值，字符串为空表示不设置
    start_date: str = "20100101"
    end_date: str = ""
    commission: float = 0.0001
    slippage: float = 0.0001
    init_cash: int = 100 * 10000
    benchmark: str = "510300.SH"

    def __str__(self):
        return self.name

    def load_datas(self):
        logger.info("开始加载数据...")  #
        loader = CSVDataloader(
            DATA_DIR.joinpath("universe"),
            self.symbols,
            start_date=self.start_date,
            end_date=self.end_date,
        )
        df = loader.load(fields=self.features, names=self.feature_names)
        df["date"] = df.index
        df.dropna(inplace=True)
        return df

    def _parse_period(self):
        module = importlib.import_module("bt.algos")
        if self.algo_period == "RunEveryNPeriods":
            algo_period = getattr(module, self.algo_period)(self.algo_period_days)
        else:
            if self.algo_period in [
                "RunWeekly",
                "RunOnce",
                "RunMonthly",
                "RunQuarterly",
                "RunYearly",
            ]:
                algo_period = getattr(module, self.algo_period)()
            else:
                algo_period = bt.algos.RunDaily()
        return algo_period

    def _parse_weights(self):
        if self.algo_weight == "WeighSpecified":
            return bt.algos.WeighSpecified(**self.algo_weight_fix)()
        else:
            module = importlib.import_module("bt.algos")
            algo_period = getattr(module, self.algo_weight)()
            return algo_period

    def get_algos(self, df_all):
        algos = []
        if self.algo_weight == "WeighERC":
            algos.append(bt.algos.RunAfterDays(days=22 * 3))
        algos.append(self._parse_period())

        if len(self.rules_buy) or len(self.rules_sell):
            algos.append(
                algos_extend.SelectBySignal(
                    df_all,
                    rules_buy=self.rules_buy,
                    buy_at_least_count=self.at_least_buy,
                    rules_sell=self.rules_sell,
                    sell_at_least_count=self.at_least_sell,
                )
            )
        else:
            algos.append(bt.algos.SelectAll())

        if self.order_by and len(self.order_by):
            signal = df_all.pivot_table(
                values=self.order_by, index=df_all.index, columns="symbol"
            )
            algos.append(algos_extend.SelectTopK(signal=signal, K=self.topK))

        algos.append(self._parse_weights())
        algos.append(bt.algos.Rebalance())
        return algos

    def to_json(self, name):
        import json
        from config import DATA_DIR

        return asdict(self)
        # with open(DATA_DIR.joinpath('tasks').joinpath(name + '.json'), "w", encoding='UTF-8') as f:
        #    json.dump(asdict(self), f, ensure_ascii=False)


def task_from_json(name):
    with open(DATA_DIR.joinpath("tasks").joinpath(name), "r", encoding="UTF-8") as f:
        json_data = json.load(f)
        return Task(**json_data)


def run_task(task):
    import warnings

    warnings.simplefilter(action="ignore", category=FutureWarning)

    df = CSVDataloader(config.DATA_DIR_QUOTES.resolve(), symbols=task.symbols).load(
        task.features, task.feature_names
    )
    df.dropna(inplace=True)
    df_close = df.pivot_table(values="close", index=df.index, columns="symbol")
    df_close.dropna(inplace=True)

    print(df_close)
    s = bt.Strategy(task.name, task.get_algos(df))
    s_bench = bt.Strategy(
        "等权-买入并持有",
        [
            bt.algos.SelectAll(),
            bt.algos.WeighEqually(),
            bt.algos.Rebalance(),
        ],
    )

    bkts = []
    stras = [s, s_bench]
    for stra in stras:
        bkt = bt.Backtest(stra, df_close, progress_bar=True)
        bkts.append(bkt)

    if task.benchmark:
        df_bench = CSVDataloader(
            config.DATA_DIR_QUOTES.resolve(), symbols=[task.benchmark]
        ).load()
        df_bench_close = df_bench.pivot_table(
            values="close", index=df_bench.index, columns="symbol"
        )
        df_bench_close.dropna(inplace=True)
        bkts.append(
            bt.Backtest(
                bt.Strategy(
                    "基准",
                    [
                        bt.algos.SelectAll(),
                        bt.algos.WeighEqually(),
                        bt.algos.Rebalance(),
                    ],
                ),
                df_bench_close,
            )
        )

    res = bt.run(*bkts)
    return res


if __name__ == "__main__":
    task = Task()
    task._id = "c087ca59-2345-4345-b3d5-12ac8fb1eeca"
    task.name = "大小盘动量轮动"
    task.desc = "沪深300与创业板 ETF的大小盘轮动，取动量大的持有。"
    task.symbols = ["510300.SH", "159915.SZ"]
    task.features = ["roc(close,20)"]
    task.feature_names = ["roc_20"]

    task.rules_buy = ["roc_20>0.02"]
    task.rules_sell = ["roc_20<-0.02"]
    task.order_by = "roc_20"
    task.algo_period = "SelectAll"
    task.algo_weight = "WeighEqually"
    task.benchmark = "000300.SH"

    import uuid

    # 生成一个随机的GUID
    guid = uuid.uuid4()
    if task._id == None:
        task._id = str(guid)

    from utils import mongo_utils
    # mongo_utils.get_db()['tasks'].update_one({"_id": task._id},update={"$set":asdict(task)},upsert=True)

    res = run_task(task)
    df = res.prices
    print(df)
    df["id"] = task._id
    df["date"] = df.index
    df["date"] = df["date"].apply(lambda x: x.strftime("%Y%m%d"))
    df["_id"] = task._id + "_" + df["date"]

    tb_equities = "task_equities"
    mongo_utils.get_db()[tb_equities].delete_many({"id": task._id})
    mongo_utils.write_df(tb_equities, df)

    df_orders = res.get_transactions()

    tb_orders = "task_orders"
    mongo_utils.get_db()[tb_orders].delete_many({"id": task._id})
