import streamlit as st
import kkweb.config as config
from task import Task, run_task
import json
import toml

def get_tasks():
    from kkweb.config import DATA_DIR
    import os
    return [ f for f in os.listdir(DATA_DIR.joinpath('tasks').resolve()) if '.toml' in f ]


def strategies():
    task_file = st.selectbox(label='请选择策略：', options=get_tasks())
    with open(config.DATA_DIR.joinpath('tasks').joinpath(task_file).resolve(), 'r', encoding='utf-8') as f:
        task = Task(**toml.load(f))
        #task = Task(**json.load(f))

    if st.button('回测'):
        st.write('启动回测：' + task.name)

        with st.spinner('回测进行中，请稍后...'):
            res = run_task(task)
            df_all = res.prices
            st.line_chart(df_all)
            df_ratios = e.get_ratios(df_all)
            st.write(df_ratios)

            orders_df = e.get_orders_df()
            st.write(orders_df)

            trades_df = e.get_trades_df()
            st.write(trades_df)