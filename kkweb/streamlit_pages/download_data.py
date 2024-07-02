import streamlit as st
import pandas as pd
import numpy as np
import os
from io import BytesIO

def download_data():
    st.title("数据下载")
    st.write("请从以下选项中选择所需的数据，并点击下载按钮获取文件。")

    # 添加超链接和搜索引擎功能
    st.markdown("""
        [Streamlit Documentation](https://docs.streamlit.io/)
        <br>
        <form action="https://www.google.com/search" method="get" target="_blank">
            <input type="text" name="q" placeholder="Search financial data" style="width: 300px; padding: 10px; font-size: 16px;">
            <input type="submit" value="Search" style="padding: 10px 20px; font-size: 16px;">
        </form>
        <br>
    """, unsafe_allow_html=True)

    # 扫描指定文件夹中的所有CSV文件并显示其标题
    @st.cache_data
    def scan_csv_files(directory):
        files = [f for f in os.listdir(directory) if f.endswith('.csv')]
        return files

    directory = "D:\\kkwebui\\kkweb\\streamlit_pages\\"
    files = scan_csv_files(directory)

    if files:
        selected_file = st.selectbox("选择CSV文件", files)
        if selected_file:
            file_path = os.path.join(directory, selected_file)
            data = pd.read_csv(file_path)

            # 解析日期列为datetime对象
            if 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])

            # 显示数据列名以供确认
            st.write("数据集中存在的列名：", data.columns.tolist())

            # 检查数据集中是否存在 'category' 列
            if 'category' in data.columns:
                st.subheader("选择数据类别")
                data_categories = data['category'].unique()
                selected_category = st.selectbox("选择类别", data_categories)
                filtered_data = data[data['category'] == selected_category]
            else:
                st.warning("数据集中不包含 'category' 列，将使用完整数据集。")
                filtered_data = data

            # 确认数据集中是否存在 'date' 列
            if 'date' in filtered_data.columns:
                st.subheader("选择日期范围")
                date_range_option = st.selectbox("选择日期范围类型", ["天", "月", "年"])
                if date_range_option == "天":
                    start_date = st.date_input("开始日期", value=pd.to_datetime("2023-01-01"))
                    end_date = st.date_input("结束日期", value=pd.to_datetime("2023-12-31"))
                elif date_range_option == "月":
                    start_date = st.date_input("选择月份（开始）", value=pd.to_datetime("2023-01-01"))
                    end_date = st.date_input("选择月份（结束）", value=pd.to_datetime("2023-12-31"))
                    start_date = pd.to_datetime(start_date).replace(day=1)
                    end_date = pd.to_datetime(end_date).replace(day=1) + pd.offsets.MonthEnd(1)
                else:
                    start_date = st.date_input("选择年份（开始）", value=pd.to_datetime("2023-01-01"))
                    end_date = st.date_input("选择年份（结束）", value=pd.to_datetime("2023-12-31"))
                    start_date = pd.to_datetime(start_date).replace(month=1, day=1)
                    end_date = pd.to_datetime(end_date).replace(month=12, day=31)

                filtered_data = filtered_data[
                    (filtered_data["date"] >= pd.to_datetime(start_date)) & (
                                filtered_data["date"] <= pd.to_datetime(end_date))]
            else:
                st.warning("数据集中不包含 'date' 列，将无法按日期过滤数据。")

            st.subheader("过滤后的数据预览")
            st.dataframe(filtered_data)

            st.subheader("下载数据")
            buffer = BytesIO()
            filtered_data.to_csv(buffer, index=False)
            buffer.seek(0)

            st.download_button(
                label="下载CSV文件",
                data=buffer,
                file_name="filtered_data.csv",
                mime="text/csv"
            )

            st.markdown("""
                <style>
                .stButton>button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 15px 32px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    transition-duration: 0.4s;
                    cursor: pointer;
                }
                .stButton>button:hover {
                    background-color: white;
                    color: black;
                    border: 2px solid #4CAF50;
                }
                </style>
            """, unsafe_allow_html=True)

            if 'date' in filtered_data.columns and 'value' in filtered_data.columns:
                st.subheader("数据图表")
                st.line_chart(filtered_data.set_index('date')["value"])
            else:
                st.warning("数据集中不包含 'date' 或 'value' 列，无法生成图表。")

            st.sidebar.header("交互式选项")
            show_data = st.sidebar.checkbox("显示原始数据", value=True)
            if show_data:
                st.sidebar.write(data)
    else:
        st.warning("没有找到CSV文件。")

if __name__ == "__main__":
    download_data()
