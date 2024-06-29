import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def strategy_display():



    # 页眉
    st.title("勇者胜-1")
    st.write("全仓买入1支票，早盘买入，第二天尾盘卖出，股票为近10日内出现过涨停的股票，主要根据技术面指标研究的选股策略。单支票仓位较重，收益波动较大，高收益与高风险并存。")

    # 筛选选项
    st.write("### 筛选时间")
    time_options = ["1月", "3月", "6月", "1年", "全部"]
    time_selection = st.selectbox("", time_options, index=4)

    # 示例数据
    dates = pd.date_range(start="2023-06-01", periods=394, freq='D')
    strategy_returns = np.cumsum(np.random.randn(394)) / 100 + 1.75
    relative_returns = np.cumsum(np.random.randn(394)) / 100 + 1.5
    benchmark_returns = np.cumsum(np.random.randn(394)) / 100

    # 策略收益图表
    st.write("### 策略收益图表")
    fig, ax = plt.subplots()
    ax.plot(dates, strategy_returns, label="策略收益率", color='red')
    ax.plot(dates, relative_returns, label="相对收益率", color='orange')
    ax.plot(dates, benchmark_returns, label="基准指数", color='blue')
    ax.fill_between(dates, strategy_returns, relative_returns, color='pink', alpha=0.3)
    ax.legend()
    st.pyplot(fig)

    # 显示数值
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="累计收益", value="175.45%")
        st.metric(label="年化收益", value="156.79%")
    with col2:
        st.metric(label="夏普比率", value="2.00")
        st.metric(label="今日收益", value="7.21%")
    with col3:
        st.metric(label="最大回撤", value="20.00%")

    # 获取代码按钮
    st.button("获取代码")

    # 策略作者
    st.write("#### 策略作者：boris58")

    # 页脚
    st.write("### 其他信息")
    st.write("这里可以添加其他相关信息和功能。")

if __name__ == "__main__":
    pass
