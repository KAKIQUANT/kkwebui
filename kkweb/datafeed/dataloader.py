from pathlib import WindowsPath

import numpy as np
import pandas as pd
from datetime import datetime

import requests
from tqdm import tqdm
import abc
from datafeed.expr import calc_expr


class Dataloader:

    def __init__(self, path, symbols, start_date='20100101', end_date=datetime.now().strftime('%Y%m%d')):
        self.symbols = symbols
        self.path = path
        self.start_date = start_date
        if not end_date or end_date == '':
            end_date = datetime.now().strftime('%Y%m%d')
        self.end_date = end_date

    @abc.abstractmethod
    def _load_dfs(self):
        pass

    def _concat_dfs(self, dfs: list):
        df = pd.concat(dfs)
        #df.dropna(inplace=True)
        df.sort_index(inplace=True)
        return df

    def _reset_index(self, df: pd.DataFrame):
        trade_calendar = list(set(df.index))
        trade_calendar.sort()

        def _ffill_df(sub_df: pd.DataFrame):
            df_new = sub_df.reindex(trade_calendar, method='ffill')
            return df_new

        df = df.groupby('symbol', group_keys=False).apply(lambda sub_df: _ffill_df(sub_df))
        return df

    def load(self, fields=None, names=None):
        dfs = self._load_dfs()
        df = self._concat_dfs(dfs)

        # df = self._reset_index(df)

        if not fields or not names or len(fields) == 0 or len(fields) != len(names):
            return df
        else:

            dfs_expr = []

            cols = []
            count = 0
            df.set_index([df.index, 'symbol'], inplace=True)
            for field, name in tqdm(zip(fields, names)):
                # print(field)

                se = calc_expr(df, field)
                count += 1
                if count < 10:
                    df[name] = se
                else:
                    se.name = name
                    cols.append(se)
            if len(cols):
                df_cols = pd.concat(cols, axis=1)
                df = pd.concat([df, df_cols], axis=1)

            df_all = df.loc[self.start_date: self.end_date].copy()
            # print(df_all.index.levels[0])
            df_all['symbol'] = df_all.index.droplevel(0)
            # df_all['symbol'] = df_all.index.levels[0]
            df_all.index = df_all.index.droplevel(1)
            return df_all


class CSVDataloader(Dataloader):
    def __init__(self, path: WindowsPath, symbols, start_date='20100101', end_date=datetime.now().strftime('%Y%m%d')):
        super(CSVDataloader, self).__init__(path, symbols, start_date, end_date)

    def _read_csv(self, symbol):
        file = symbol + '.csv'
        df = pd.read_csv(self.path.joinpath(file), index_col=None)
        df['date'] = df['date'].apply(lambda x: str(x))
        df.set_index('date', inplace=True)
        df['symbol'] = symbol
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True, ascending=True)
        df = df.loc[self.start_date:, :]
        return df

    def _load_dfs(self):
        dfs = []
        for s in self.symbols:
            df = self._read_csv(s)
            dfs.append(df)
        return dfs


if __name__ == '__main__':
    import config
    import numpy as np

    fields = ['signed_power(signed_power(close, 40)*ts_max(low, 20)/ts_rank(open, 40)-low-10, 40)']
    names = ['expr']
    df = CSVDataloader(config.DATA_DIR_QUOTES.resolve(), symbols=['159915.SZ', '510300.SH']).load(fields, names)

    print(df)
