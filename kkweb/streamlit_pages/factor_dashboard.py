import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import time
import threading
import queue

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

    data_performance = {
        "date": pd.date_range(start="2019-01-01", end="2019-12-30", freq='D'),
        "1分位数": [1.25 + 0.01 * i for i in range(365)],
        "2分位数": [1.27 + 0.01 * i for i in range(365)],
        "3分位数": [1.28 + 0.01 * i for i in range(365)],
        "4分位数": [1.27 + 0.01 * i for i in range(365)],
        "5分位数": [1.28 + 0.01 * i for i in range(365)],
        "最小-最大分位": [0.98 + 0.01 * i for i in range(365)]
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

    # Display dynamic stock graphs section
    st.header("其他股票图表展示")

    other_stocks_data = {
        "stock1": {
            "date": pd.date_range(start="2019-01-01", end="2019-12-30", freq='D'),
            "value": [1.1 + 0.02 * i for i in range(365)]
        },
        "stock2": {
            "date": pd.date_range(start="2019-01-01", end="2019-12-30", freq='D'),
            "value": [1.2 + 0.015 * i for i in range(365)]
        },
        "stock3": {
            "date": pd.date_range(start="2019-01-01", end="2019-12-30", freq='D'),
            "value": [1.15 + 0.018 * i for i in range(365)]
        }
    }

    # Ensure all arrays in other_stocks_data have the same length
    for stock in other_stocks_data:
        min_length = min(len(other_stocks_data[stock][col]) for col in other_stocks_data[stock])
        for col in other_stocks_data[stock]:
            other_stocks_data[stock][col] = other_stocks_data[stock][col][:min_length]

    placeholder = st.empty()

    # Create a queue for chart updates
    chart_queue = queue.Queue()
    stop_event = threading.Event()

    # Create a thread for generating charts
    chart_thread = threading.Thread(target=generate_charts, args=(chart_queue, other_stocks_data, stop_event))
    chart_thread.start()

    # Display rankings
    st.header("因子值最小的20只股票 (2019-12-30)")
    st.table(df_small)

    st.header("因子值最大的20只股票 (2019-12-30)")
    st.table(df_large)

    # Process chart updates from the queue
    while True:
        chart = chart_queue.get()
        if chart is None:
            break
        with placeholder.container():
            st.altair_chart(chart, use_container_width=True)
        time.sleep(1)  # Ensure the app keeps updating

if __name__ == "__main__":
    try:
        dashboard()
    finally:
        stop_event.set()
