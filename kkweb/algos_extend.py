import bt
import pandas as pd


class SelectBySignal(bt.Algo):
    def __init__(self, df, rules_buy=[], buy_at_least_count=1, rules_sell=[], sell_at_least_count=1):
        super(SelectBySignal, self).__init__()
        self.rules_buy = rules_buy
        self.rules_sell = rules_sell
        self.df = df

        if buy_at_least_count > len(rules_buy):
            buy_at_least_count = len(rules_buy)
        if buy_at_least_count <= 0:
            buy_at_least_count = 1
        self.buy_at_least_count = buy_at_least_count

        if sell_at_least_count > len(rules_sell):
            sell_at_least_count = len(rules_sell)
        if sell_at_least_count <= 0:
            sell_at_least_count = 1
        self.sell_at_least_count = sell_at_least_count

    def _check_if_matched(self, df_bar, rules, at_least_count):

        se_count = pd.Series(index=df_bar.index, data=0)
        for r in rules:
            se_count += df_bar.eval(r)

        matched_items = se_count[(se_count.values >= at_least_count)].index
        return list(matched_items)

    def __call__(self, target):
        if len(self.rules_buy) == 0 and len(self.rules_sell) == 0:
            return True

        df_bar = self.df.loc[target.now]
        if type(df_bar) is pd.Series:
            df_bar = df_bar.to_frame().T
        df_bar.set_index('symbol', inplace=True)
        for c in df_bar.columns:
            df_bar.loc[:, c] = df_bar[c].astype(float)
        # df_bar['roc_20'] = df_bar['roc_20'].astype(float)
        matched_buy = []
        matched_sell = []
        if self.rules_buy and len(self.rules_buy):
            matched_buy = self._check_if_matched(df_bar, self.rules_buy, self.buy_at_least_count)
        else:
            matched_buy = list(df_bar.index)  # 没有配置买入规则，但有卖出，就是选全选。

        if self.rules_sell and len(self.rules_sell):
            matched_sell = self._check_if_matched(df_bar, self.rules_sell, self.sell_at_least_count)

        #holdings = context.portfolio.positions.keys()
        if target.now in target.positions.index:
            sig = target.positions.loc[target.now] > 0
            holdings = list(sig[sig == True].index)  # noqa: E712
        else:
            holdings = []

        # holdings = target.get_long_symbols(target.ctxs)
        if holdings and len(holdings) > 0:
            matched_buy += holdings
            matched_buy = list(set(matched_buy))

        if matched_sell:
            for sell in matched_sell:
                if sell in matched_buy:
                    matched_buy.remove(sell)

        matched_buy = list(set(matched_buy))
        target.temp['selected'] = matched_buy
        # if len(matched_buy) > 1:
        #    print(matched_buy)
        return True


class SelectTopK(bt.AlgoStack):
    def __init__(self, signal, K, sort_descending=True, all_or_none=False, filter_selected=True):
        super(SelectTopK, self).__init__(bt.algos.SetStat(signal),
                                         bt.algos.SelectN(K, sort_descending, all_or_none, filter_selected))


class SelectHoldingExcludeWhere(bt.Algo):
    def __init__(self, signal, include_no_data=False, include_negative=False):
        super(SelectHoldingExcludeWhere, self).__init__()
        if isinstance(signal, pd.DataFrame):
            self.signal_name = None
            self.signal = signal
        else:
            self.signal_name = signal
            self.signal = None

        self.include_no_data = include_no_data
        self.include_negative = include_negative

    def calc_signal(self, target):
        if self.signal_name is None:
            signal = self.signal
        else:
            signal = target.get_data(self.signal_name)

        if target.now in signal.index:
            sig = signal.loc[target.now]
            # get tickers where True
            # selected = sig.index[sig]
            selected = sig[sig == True].index  # noqa: E712
            # save as list
            if not self.include_no_data:
                universe = target.universe.loc[target.now, list(selected)].dropna()
                if self.include_negative:
                    selected = list(universe.index)
                else:
                    selected = list(universe[universe > 0].index)
            return list(selected)

    def __call__(self, target):

        holding = []
        if target.now in target.positions.index:
            sig = target.positions.loc[target.now] > 0
            holding_list = sig[sig == True].index  # noqa: E712
            if not self.include_no_data:
                universe = target.universe.loc[target.now, list(holding_list)].dropna()
                if self.include_negative:
                    holding_list = list(universe.index)
                else:
                    holding_list = list(universe[universe > 0].index)

        select_by_signal = self.calc_signal(target)  # 这是符合卖出策略

        if 'selected' not in target.temp.keys():
            all = target.temp['selected']
        else:
            all = target.universe.columns

        selected = target.temp['selected']
        selected = list(set(selected + holding))
        target.temp['selected'] = selected
        return True
