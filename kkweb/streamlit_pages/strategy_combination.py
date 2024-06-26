import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



def generate_strategy_data(seed, periods=394):
    np.random.seed(seed)
    dates = pd.date_range('2022-01-01', periods=periods)
    return pd.DataFrame({
        'Date': dates,
        'Strategy Return': (np.random.randn(periods).cumsum() + 100) * 1.75,
        'Relative Return': (np.random.randn(periods).cumsum() + 100) * 1.5,
        'Benchmark': (np.random.randn(periods).cumsum() + 100) * 1.2,
        '沪深300指数': (np.random.randn(periods).cumsum() + 100) * 1.3
    })

def strategy_evaluation(strategy_name, display_data, data_source):
    cumulative_return = (display_data[data_source].iloc[-1] / display_data[data_source].iloc[0] - 1) * 100
    annualized_return = ((1 + cumulative_return / 100) ** (365 / len(display_data)) - 1) * 100
    max_drawdown = ((display_data[data_source].min() / display_data[data_source].max()) - 1) * 100
    today_return = display_data[data_source].pct_change().iloc[-1] * 100
    sharpe_ratio = (annualized_return - 2) / display_data[data_source].std()
    sortino_ratio = (annualized_return - 2) / display_data[data_source][display_data[data_source] < 0].std()
    volatility = display_data[data_source].std() * np.sqrt(252)

    st.metric(label=f"{strategy_name} 累计划收益", value=f"{cumulative_return:.2f}%")
    st.metric(label=f"{strategy_name} 年化收益", value=f"{annualized_return:.2f}%")
    st.metric(label=f"{strategy_name} 今日收益", value=f"{today_return:.2f}%")
    st.metric(label=f"{strategy_name} 最大回撤", value=f"{max_drawdown:.2f}%")
    st.metric(label=f"{strategy_name} 夏普比率", value=f"{sharpe_ratio:.2f}")
    st.metric(label=f"{strategy_name} 索提诺比率", value=f"{sortino_ratio:.2f}")
    st.metric(label=f"{strategy_name} 波动率", value=f"{volatility:.2f}%")

def display_strategy(strategy_name, data):
    # 选择数据源
    st.sidebar.header(f"选择数据源 - {strategy_name}")
    data_source = st.sidebar.selectbox(
        f"数据源 - {strategy_name}",
        ["Strategy Return", "Relative Return", "Benchmark", "沪深300指数"]
    )

    # 数据展示
    st.subheader(f"数据展示 - {strategy_name}")

    # 选择时间范围
    time_range = st.selectbox(f"缩放时间 - {strategy_name}", ["1月", "3月", "6月", "1年", "全部"], index=4)
    if time_range == "1月":
        display_data = data.tail(30)
    elif time_range == "3月":
        display_data = data.tail(90)
    elif time_range == "6月":
        display_data = data.tail(180)
    elif time_range == "1年":
        display_data = data.tail(365)
    else:
        display_data = data

    # 策略评价
    st.header(f"策略评价 - {strategy_name}")
    st.write(f"{strategy_name} 表现优异，累计划收益和年化收益均表现出色，风险控制得当，最大回撤较低。夏普比率和索提诺比率均显示出策略的高收益与低风险特性。")

    # 页面布局分割
    col1, col2 = st.columns((3, 1))

    with col1:
        # 可交互图表
        st.header(f"策略收益图 - {strategy_name}")
        fig = go.Figure()
        for source in ["Strategy Return", "Relative Return", "Benchmark", "沪深300指数"]:
            fig.add_trace(go.Scatter(x=display_data['Date'], y=display_data[source], mode='lines', name=source))
        fig.update_layout(title=f"{data_source}随时间变化", xaxis_title='日期', yaxis_title='收益率')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 数据统计
        st.header(f"数据统计 - {strategy_name}")
        strategy_evaluation(strategy_name, display_data, data_source)

    # 增加其他类型图表
    st.header(f"更多图表 - {strategy_name}")
    chart_type = st.selectbox(f"选择图表类型 - {strategy_name}", ["收益率分布图", "累积收益率", "其它类型"])
    fig_size = st.slider(f"选择图表大小 - {strategy_name}", 200, 800, 400)

    if chart_type == "收益率分布图":
        fig2 = px.histogram(display_data, x=data_source, nbins=50, title="收益率分布")
        fig2.update_layout(width=fig_size, height=fig_size)
        st.plotly_chart(fig2, use_container_width=True)
    elif chart_type == "累积收益率":
        fig3 = px.line(display_data, x='Date', y=data_source, title="累积收益率")
        fig3.update_layout(width=fig_size, height=fig_size)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        fig4 = px.scatter(display_data, x='Date', y=data_source, title="其它类型")
        fig4.update_layout(width=fig_size, height=fig_size)
        st.plotly_chart(fig4, use_container_width=True)

    # 下载、收藏和获取代码按钮放在更多图表部分的底端
    col3, col4, col5 = st.columns(3)
    with col3:
        st.download_button(
            label=f"下载数据 - {strategy_name}",
            data=display_data.to_csv().encode('utf-8'),
            file_name=f'{strategy_name}_data.csv',
            mime='text/csv',
        )
    with col4:
        st.button(f"收藏 - {strategy_name}")
    with col5:
        st.button(f"获取代码 - {strategy_name}")

def build_strategy():
    # 页面标题
    st.title("Strategy Sharing")

    # 生成多个策略数据
    strategy_data = {
        "策略1": generate_strategy_data(42),
        "策略2": generate_strategy_data(43),
        "策略3": generate_strategy_data(44),
        "策略4": generate_strategy_data(45),
        "策略5": generate_strategy_data(46)
    }

    for strategy_name, data in strategy_data.items():
        display_strategy(strategy_name, data)
        st.markdown("---")  # 分隔线

if __name__ == "__main__":
    build_strategy()
