from config import DATA_DIR
import streamlit as st
import os
from datafeed.dataloader import CSVDataloader
from datafeed.alphalens.streamit_tears import create_full_tear_sheet
from datafeed.alphalens.utils import get_clean_factor_and_forward_returns
def build_page():
    instru = DATA_DIR.joinpath('instruments')


    files = os.listdir(instru.resolve())
    filename = st.selectbox('请选择投资标的集合:', options=files)
    with open(instru.joinpath(filename).resolve(), 'r') as f:
        symbols = f.readlines()

    symbols = [s.replace('\n', '') for s in symbols]
    st.write(symbols)
    factor_expr = st.text_input('请输入因子表达式', value='roc(close,20)')
    if st.button('加载数据并计算因子值'):
        loader = CSVDataloader(DATA_DIR.joinpath('quotes'), symbols)
        df = loader.load(fields=[factor_expr], names=['factor_name'])
        factor_df = df[['symbol', 'factor_name']]
        factor_df.set_index([factor_df.index, 'symbol'], inplace=True)
        close_df = df.pivot_table(values='close', index='date', columns='symbol')



        results = get_clean_factor_and_forward_returns(factor_df, close_df)



        create_full_tear_sheet(results)