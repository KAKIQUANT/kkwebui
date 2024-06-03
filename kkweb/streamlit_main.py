from streamlit_option_menu import option_menu
from streamlit_pages.page_analysis import build_page
from streamlit_pages import page_create_task
import streamlit as st
import os
from kkweb.config import DATA_DIR
from task import task_from_json


from task import Task

st.set_page_config(page_title='Quantlab - AI量化实验室', page_icon=":bar_chart:", layout='wide')
# params = st.query_params
# st.write(params)
token = None

# 定义边栏导航
with st.sidebar:
    # https://icons.getbootstrap.com/
    choose = option_menu('Quantlab-AI量化实验室', ['创建策略向导'],#,'策略集合', '时间序列分析', '单因子分析'
                         icons=['bar-chart'])#, 'boxes', 'caret-right', 'fingerprint'

    page_create_task.show_tasks()
    #st.write(page_create_task.task_)

if choose == '时间序列分析':
    build_page()

if choose == '创建策略向导':
    page_create_task.build()

from streamlit_pages.page_strategies import strategies

if choose == '策略集合':
    strategies()


elif choose == "单因子分析":
    from kkwebui.config import DATA_DIR

    instru = DATA_DIR.joinpath('instruments')
    import os

    files = os.listdir(instru.resolve())
    filename = st.selectbox('请选择投资标的集合:', options=files)
    with open(instru.joinpath(filename).resolve(), 'r') as f:
        symbols = f.readlines()

    symbols = [s.replace('\n', '') for s in symbols]
    st.write(symbols)
    factor_expr = st.text_input('请输入因子表达式', value='slope(close,20)')
    if st.button('加载数据并计算因子值'):
        from datafeed.dataloader import CSVDataloader

        loader = CSVDataloader(DATA_DIR.joinpath('universe'), symbols)
        df = loader.load(fields=[factor_expr], names=['factor_name'])
        factor_df = df[['symbol', 'factor_name']]
        factor_df.set_index([factor_df.index, 'symbol'], inplace=True)
        close_df = df.pivot_table(values='close', index='date', columns='symbol')
        # st.write(factor_df)
        # st.write(close_df)

        from datafeed.alphalens.utils import get_clean_factor_and_forward_returns

        results = get_clean_factor_and_forward_returns(factor_df, close_df)
        st.write(results)

        from datafeed.alphalens.streamit_tears import create_full_tear_sheet

        create_full_tear_sheet(results)
