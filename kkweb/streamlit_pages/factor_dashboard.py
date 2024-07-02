import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import threading
import queue
from streamlit_pages import single_factor_analysis

def generate_charts(chart_queue, other_stocks_data, stop_event):
    while not stop_event.is_set():
        for stock, data in other_stocks_data.items():
            df_stock = pd.DataFrame(data)
            chart = alt.Chart(df_stock).mark_line().encode(
                x='date:T',
                y='value:Q'
            ).properties(title=f'{stock}表现折线图')
            chart_queue.put(chart)
            time.sleep(5)
            if stop_event.is_set():
                break
    chart_queue.put(None)  # Signal the end of chart generation

def generate_other_charts(chart_queue, other_data, stop_event):
    while not stop_event.is_set():
        for name, data in other_data.items():
            df_other = pd.DataFrame(data)
            chart = alt.Chart(df_other).mark_bar().encode(
                x='date:T',
                y='value:Q'
            ).properties(title=f'{name} 表现柱状图')
            chart_queue.put(chart)
            time.sleep(5)
            if stop_event.is_set():
                break
    chart_queue.put(None)  # Signal the end of chart generation

def dashboard():
    # Load data (replace with actual data loading)
    data_ranking_small = {
        "股票名称": ["重庆钢铁", "中远海发", "中国一重", "招商南油", "海油发展"],
        "股票代码": ["601005.SHA", "601866.SHA", "601106.SHA", "601975.SHA", "600968.SHA"],
        "因子值": [1.9020, 2.5748, 2.8763, 2.8843, 2.9370]
    }

    data_ranking_large = {
        "股票名称": ["辣园股份", "长春高新", "福耀玻璃", "万华化学", "平安银行"],
        "股票代码": ["600655.SHA", "000661.SZA", "600660.SHA", "600309.SHA", "000001.SZA"],
        "因子值": [1591.9062, 1640.4613, 1737.8302, 1768.4532, 1776.9872]
    }

    yz = pd.read_csv('D:\\kkwebui\\kkweb\\streamlit_pages\\因子数据.csv')
    yz = yz.iloc[:243]
    data_performance = {
        "date": pd.date_range(start="2024-02-28", end="2024-07-01", freq='D'),
        "600196.XSHG": yz['600196.XSHG'].to_list(),
        "600703.XSHG": yz['600703.XSHG'].to_list(),
        "601088.XSHG": yz['601088.XSHG'].to_list(),
        "601108.XSHG": yz['601108.XSHG'].to_list(),
        "601398.XSHG": yz['601398.XSHG'].to_list(),
        "000625.XSHE": yz['000625.XSHE'].to_list()
    }

    # Ensure all arrays are the same length
    min_length = min(len(data_performance[col]) for col in data_performance)
    for col in data_performance:
        data_performance[col] = data_performance[col][:min_length]

    df_small = pd.DataFrame(data_ranking_small)
    df_large = pd.DataFrame(data_ranking_large)
    df_performance = pd.DataFrame(data_performance)

    # Streamlit layout
    st.title("因子值排名和表现概览")

    # Display performance chart
    st.header("因子表现概览")

    chart_type = st.selectbox("选择图表类型", ["折线图", "柱状图", "散点图"])

    if chart_type == "折线图":
        chart = alt.Chart(df_performance.melt('date')).mark_line().encode(
            x='date:T',
            y='value:Q',
            color='variable:N'
        ).properties(title='因子表现折线图')
    elif chart_type == "柱状图":
        chart = alt.Chart(df_performance.melt('date')).mark_bar().encode(
            x='date:T',
            y='value:Q',
            color='variable:N'
        ).properties(title='因子表现柱状图')
    elif chart_type == "散点图":
        chart = alt.Chart(df_performance.melt('date')).mark_point().encode(
            x='date:T',
            y='value:Q',
            color='variable:N'
        ).properties(title='因子表现散点图')

    st.altair_chart(chart, use_container_width=True)
    if st.button('know more'):
        single_factor_analysis.build_page()

    # Display dynamic stock graphs section
    st.header("其他股票图表展示")

    zz = pd.read_csv('D:\\kkwebui\\kkweb\\streamlit_pages\\(中证800)_副本.csv', usecols=['date', 'close'])
    zz = zz[(zz['date'] >= '2019-01-01') & (zz['date'] <= '2019-12-30')]
    other_stocks_data = {
        "中证800": {
            "date": pd.date_range(start="2019-01-01", end="2019-12-30", freq='D'),
            "value": zz['close'].tolist()
        }
    }

    other_data = {
        "假数据1": {
            "date": pd.date_range(start="2024-01-01", end="2024-06-30", freq='D'),
            "value": np.random.rand(181).tolist()
        },
        "假数据2": {
            "date": pd.date_range(start="2024-01-01", end="2024-06-30", freq='D'),
            "value": np.random.rand(181).tolist()
        },
        "假数据3": {
            "date": pd.date_range(start="2024-01-01", end="2024-06-30", freq='D'),
            "value": np.random.rand(181).tolist()
        }
    }

    # Ensure all arrays in other_stocks_data have the same length
    for stock in other_stocks_data:
        min_length = min(len(other_stocks_data[stock][col]) for col in other_stocks_data[stock])
        for col in other_stocks_data[stock]:
            other_stocks_data[stock][col] = other_stocks_data[stock][col][:min_length]

    placeholder1 = st.empty()
    placeholder2 = st.empty()

    # Create queues for chart updates
    chart_queue1 = queue.Queue()
    chart_queue2 = queue.Queue()
    stop_event = threading.Event()

    # Create threads for generating charts
    chart_thread1 = threading.Thread(target=generate_charts, args=(chart_queue1, other_stocks_data, stop_event))
    chart_thread2 = threading.Thread(target=generate_other_charts, args=(chart_queue2, other_data, stop_event))
    chart_thread1.start()
    chart_thread2.start()

    # Display rankings
    st.header("因子值最小的20只股票 (2019-12-30)")
    st.table(df_small)

    st.header("因子值最大的20只股票 (2019-12-30)")
    st.table(df_large)

    # Process chart updates from the queues
    while True:
        chart1 = chart_queue1.get()
        chart2 = chart_queue2.get()
        if chart1 is None or chart2 is None:
            break
        with placeholder1.container():
            st.altair_chart(chart1, use_container_width=True)
        with placeholder2.container():
            st.altair_chart(chart2, use_container_width=True)
        time.sleep(1)  # Ensure the app keeps updating

if __name__ == "__main__":
    try:
        dashboard()
    finally:
        stop_event.set()
