import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
def database():
    # Sample data
    import streamlit as st
    import pandas as pd

    # Sample data to mimic the extended dataset
    data = {
        "因子名": ["Alpha191因子第154个", "全天特大单主动买入", "Alpha191因子第17个", "Alpha191因子第123个",
                   "Alpha191因子第101个", "Alpha191因子第4个", "全天特大单的主动卖出"],
        "1年多头收益率": [99.73, 59.13, 30.51, 31.85, 46.12, 42.98, 29.32],
        "1月多头收益率": [-1.43, 3.95, 18.96, 8.46, 3.55, -10.91, 4.66],
        "3月多头收益率": [22.79, 15.32, 6.58, 12.51, 6.40, -8.87, 20.29],
        "1年空头收益率": [47.23, 33.29, 26.97, 20.93, 20.05, 19.54, 18.95],
        "因子描述": ["因子分类: Alpha191因子第154个；具体请参考...",
                     "因子分类: 预测计算高频因子；因子简介：全天特大单主动买...",
                     "因子分类: Alpha191因子第17个；具体请参考...", "因子分类: Alpha191因子第123个；具体请参考...",
                     "因子分类: Alpha191因子第101个；具体请参考...", "因子分类: Alpha191因子第4个；具体请参考...",
                     "因子分类: 预测计算高频因子；因子简介：全天特大单的计买..."],
        "起始时间": ["2024-02-28", "2024-02-29", "2024-02-29", "2024-02-29", "2024-02-28", "2024-02-28", "2024-02-29"],
        "更新时间": ["2024-06-20", "2024-05-28", "2024-03-20", "2024-05-28", "2024-06-20", "2024-06-20", "2024-05-28"],
        "IC": [0.0091, -0.0031, 0.0128, 0.0007, 0.0088, 0.0011, -0.0005],
        "多头IC": [0.0099, 0.0026, 0.0054, 0.0068, 0.0054, 0.0045, 0.0065],
        "多头Rank IC": [-0.0025, -0.0009, -0.0008, -0.0004, -0.0006, -0.0005, -0.0007],
        "空头IR": [1.2, -0.8, 1.0, 0.5, 0.9, 0.3, -0.4],
        "多空IR": [1.5, 0.7, 1.1, 0.6, 1.0, 0.4, -0.2],
        "多头换手率": [0.35, 0.28, 0.30, 0.25, 0.33, 0.27, 0.29],
        "空头换手率": [0.32, 0.30, 0.29, 0.27, 0.31, 0.28, 0.26],
        "多空换手率": [0.67, 0.58, 0.59, 0.52, 0.64, 0.55, 0.55],
        "比较基准": ["基准A", "基准B", "基准A", "基准B", "基准A", "基准B", "基准A"],
        "分组数量": [5, 5, 5, 5, 5, 5, 5],
        "股票池": ["股票池A", "股票池B", "股票池A", "股票池B", "股票池A", "股票池B", "股票池A"],
        "3日多头IC": [0.007, 0.005, 0.008, 0.006, 0.007, 0.004, 0.006]
    }

    # Convert the data into a DataFrame
    df = pd.DataFrame(data)

    # Streamlit app layout
    st.title('因子数据库')




    # Filter options

    factor_type = st.selectbox('选择目录', ['系统因子', '社区因子'])

    filter_column = st.selectbox('筛选列', df.columns.tolist())
    filter_condition = st.selectbox('筛选条件', ['大于', '小于', '等于'])
    filter_value = st.text_input('筛选值')
    if factor_type == '系统因子':

        label = '请问您喜欢吃什么水果'
        opt = ('橘子', '苹果')

        help = '选择您喜欢吃的水果'

    else:

        label = '请问您喜欢吃什么水果'
        opt = ('橘子', '苹果', '香蕉', '草莓', '葡萄')

        help = '选择您喜欢吃的水果'

    options = st.multiselect(
        label=label,
        options=opt,

        help='选择您喜欢吃的水果'
    )

    st.write('您喜欢吃的是', options)
    # Apply filters
    if filter_value:
        try:
            filter_value = float(filter_value)
            if filter_condition == '大于':
                filtered_df = df[df[filter_column].astype(float) > filter_value]
            elif filter_condition == '小于':
                filtered_df = df[df[filter_column].astype(float) < filter_value]
            else:
                filtered_df = df[df[filter_column].astype(float) == filter_value]
        except ValueError:
            filtered_df = df[df[filter_column] == filter_value]
    else:
        filtered_df = df

    # Sorting options
    sort_column = st.selectbox('排序列', df.columns.tolist())
    ascending = st.checkbox('升序排列', value=True)

    # Sort the data
    sorted_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

    # Display sorted data
    st.dataframe(sorted_df)

    # Display factor performance metrics
    st.markdown('## 因子表现')
    st.dataframe(sorted_df[
                     ['因子名', '1年多头收益率', '1月多头收益率', '3月多头收益率', '1年空头收益率', 'IC', '多头IC',
                      '多头Rank IC', '空头IR', '多空IR', '多头换手率', '空头换手率', '多空换手率', '比较基准',
                      '分组数量', '股票池', '3日多头IC']])

    # Factor comparison and strategy generation
    st.markdown('### 因子比较')
    selected_factors = st.multiselect('选择因子进行比较', sorted_df['因子名'].tolist())

    if selected_factors:
        comparison_df = sorted_df[sorted_df['因子名'].isin(selected_factors)]
        st.dataframe(comparison_df)

    # Placeholder buttons (functionality to be implemented)
    st.button('一键生成策略')
    st.button('因子绩效对比')

    # Clear filter conditions
    if st.button('清空条件'):
        st.experimental_rerun()

