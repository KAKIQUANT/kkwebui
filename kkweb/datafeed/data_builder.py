import pandas as pd
import akshare as ak
from config import DATA_DIR


def load_astock_index(symbol):
    code = symbol[-2:].lower() + symbol[:6]
    print(code)

    df = ak.stock_zh_index_daily(symbol=code)
    df['symbol'] = symbol
    df['date'] = df['date'].apply(lambda x: str(x).replace('-', ''))
    print(df)

    df.to_csv(DATA_DIR.joinpath('quotes').joinpath(symbol + '.csv'), index=None)


basic_csvs = {'index': 'index.csv'} # 'global_index': 'global_index.csv'


def load_basic_file(filename):
    file = DATA_DIR.joinpath('basic').joinpath(filename).resolve()
    df = pd.read_csv(file)
    return df


def build_data():
    for type, filename in basic_csvs.items():
        df = load_basic_file(filename)
        if type == 'index':
            for i, row in df.iterrows():
                load_astock_index(row['symbol'])


def get_basic_list():
    all_dict = {}
    for type, filename in basic_csvs.items():
        df = load_basic_file(filename)
        df['type'] = type
        items = df.to_dict(orient='records')
        for item in items:
            all_dict.update({item['symbol']: item})
    return all_dict


if __name__ == '__main__':
    all = get_basic_list()
    print(all)
