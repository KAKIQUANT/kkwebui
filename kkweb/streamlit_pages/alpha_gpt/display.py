from loguru import logger
import streamlit as st
from langchain_openai import ChatOpenAI
import os
import json
import graphviz
from kkweb.datafeed.dataloader import CSVDataloader
from kkweb.config import DATA_DIR
from kkweb.datafeed.alphalens.streamit_tears import create_full_tear_sheet, create_information_tear_sheet, create_returns_tear_sheet, create_turnover_tear_sheet
from kkweb.datafeed.alphalens.utils import get_clean_factor_and_forward_returns
symbols = ['000300.SH','000905.SH']

def txt_to_list(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]

def alpha_factor_graph(expr: str):
    pass

sample_json = """
            {
            "expr": 生成的因子表达式,函数必须严格使用样例数据里的函数
            "desc": 对该因子表达式的解释说明
            }
        """
sources = txt_to_list("agents/worldquant_101.txt")


optional_params = {"response_format": {"type": "json_object"}}
model = "moonshot-v1-32k"
api_key = os.environ["OPENAI_API_KEY"]
base_url = "https://api.moonshot.cn/v1"
max_retries = 1

llm = ChatOpenAI(
            temperature=0,
            openai_api_key=api_key,
            model=model,
            base_url=base_url,
            max_retries=max_retries,
            model_kwargs=optional_params,
        )


def main():
    st.title("Alpha GPT - 专注因子分析")
    st.sidebar.write("### 说明")
    st.sidebar.write(
        """
        - 提出与因子分析相关的具体问题。
        - 提供明确的需求描述。
        - 如果问题不涉及因子分析，系统将拒绝回答。
        """
    )
    logger.info("App started")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if input := st.chat_input("请描述您的因子分析需求"):
        prompt = [
                        {
                            "role": "system",
                            "content": "你是一个量化分析师，用中文回复中文提问. 你可以通过阅读多个alpha因子表达式，"
                            """总结其内在规律，并且可以创新性的生成可用的因子表达式。对于生成的表达式，
                            你能够解释其有效性，并且能够用清晰简洁的语言解释其各个变量的含义。
                            你有权拒绝用户不相关，不合法的提问
                            指令描述: 根据用户需求user content生成因子表达式，如果user content 和因子无关，请拒绝回答"""
                            f"样例数据：{sources}\n"
                            "你的任务学习以上资源之后，总结其规律，输出一个同类型表达式。"
                            "书写表达式时，必须使用样例数据出现过的函数，不兼容的函数会导致报错，每次生成一个表达式，不要带Alpha#xxx,因子的相关性要低\n"
                            "Please return nothing but a JSON in the following format if you study the user input:"
                            f"{sample_json} "
                            "If the user input is not related to factor analysis, please reject the question：{error_message: '不相关'}\n"
                        },
                        {
                            "role": "user",
                            "content": f"{input}\n"
                        },
                    ]
        if st.session_state.messages == []:
            st.session_state.messages = prompt
        else:
            st.session_state.messages.append({"role": "user", "content": input})
        logger.info(f"User input: {input}")
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        with st.chat_message("assistant"):
            with st.spinner("生成中..."):
                
                try:
                    lc_messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
                    logger.debug(f"Request: {lc_messages}")
                    response = llm.invoke(lc_messages).content
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    logger.info(f"Response: {response}")
                    # Construct the response as a dictionary
                    response = json.loads(response)

                    if "error_message" in response:
                        st.warning("问题不相关，已拒绝回答。")
                    else:
                        st.write(f"因子表达式: {response['expr']}\n\n解释: {response['desc']}")
                        if True:
                            # 测试因子表达式
                            factor_expr = response['expr']
                            # factor_expr = "((close - open) / ((high - low) + .001))"
                            loader = CSVDataloader(DATA_DIR.joinpath('quotes'), symbols)
                            df = loader.load(fields=[factor_expr], names=['factor_name'])
                            factor_df = df[['symbol', 'factor_name']]
                            factor_df.set_index([factor_df.index, 'symbol'], inplace=True)
                            close_df = df.pivot_table(values='close', index='date', columns='symbol')
                            factor_data = get_clean_factor_and_forward_returns(factor_df, close_df)
                            tab1, tab2, tab3 = st.tabs(
                                ["收益分析", "信息分析", "换手率分析"]
                            )
                            long_short = True
                            group_neutral = False
                            with tab1:
                                create_returns_tear_sheet(factor_data, long_short, group_neutral)
                            with tab2:
                                create_information_tear_sheet(factor_data, group_neutral)
                            with tab3:
                                create_turnover_tear_sheet(factor_data)
                except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": str(e)})
                    st.error("生成响应时发生错误。")
                    logger.error(f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()
