import pandas as pd
import streamlit as st
from config import DATA_DIR

from kkdatac.data_builder import get_basic_list


@st.cache_data
def load_basic_list():
    return get_basic_list()


def func_basic(x):
    item = load_basic_list()[x]
    return '{}|{}'.format(item['name'], item['symbol'])


def build_page():
    st.write('时间序列风险，收益分析')
    symbols = st.multiselect(label='请选择投资标的', default=['000300.SH'], options=list(load_basic_list().keys()),
                             format_func=lambda x: func_basic(x))
    if len(symbols) == 0:
        return

    cols = []
    for s in symbols:
        df = pd.read_csv(DATA_DIR.joinpath('quotes').joinpath('{}.csv'.format(s)))
        df['date'] = df['date'].apply(lambda x: str(x))
        df.index = df['date']
        se = df['close']
        se.name = s
        cols.append(se)

    print(len(cols))
    all = pd.concat(cols, axis=1)
    #print(all)



    all.sort_values(by='date', ascending=True, inplace=True)
    all.dropna(inplace=True)
    equity = (all.pct_change() + 1).cumprod()
    #print(equity)
    equity.dropna(inplace=True)
    if len(symbols) == 1:
        # 将累积收益的Series转换为DataFrame，并添加日期列
        equity = pd.DataFrame({'equity': equity[symbols[0]]})
        #equity.set_index('date')
        st.line_chart(equity['equity'])
    else:
        #print(type(equity))
        st.line_chart(equity)

    df_ratio, df_corr = PerformanceUtils().calc_equity(df_equity=equity)

    col1, col2 = st.columns(2)
    with col1:
        st.write(df_ratio)
    with col2:
        st.write(df_corr)
