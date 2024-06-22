import os
import streamlit as st
import logging
import time
from loguru import logger
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.adapters.openai import convert_openai_messages
import json

# Set up OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk-H3MkimLzxvofEhZOfGKTveqFqDqfSa6p5vqsHwZv6lkAlLE5'
KEY = os.environ['OPENAI_API_KEY']

# Initialize OpenAI client
client = OpenAI(
    api_key=KEY,
    base_url="https://api.moonshot.cn/v1",
)

# Streamlit page configuration
st.set_page_config(page_title="Alpha GPT", page_icon="🧠", layout="wide")
st.title("Alpha GPT")

# Initialize chat history in session state if not already present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define the FactorGPTAgent class
class FactorGPTAgent:
    def __init__(self, user_prompt):
        self.sources = self.read_file_2_list('./agents/worldquant_101.txt')
        self.user_prompt = user_prompt
        optional_params = {
            "response_format": {"type": "json_object"}
        }
        self.model = ChatOpenAI(
            temperature=0,
            openai_api_key=KEY.strip(),
            model='moonshot-v1-8k',
            base_url="https://api.moonshot.cn/v1",
            max_retries=1,
            model_kwargs=optional_params
        )

    def read_file_2_list(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]

    def build_prompt(self):
        prompt = [{
            "role": "system",
            "content": (
                "你是一个量化分析师. 你可以通过阅读多个alpha因子表达式，总结其内在规律，并且可以创新性的生成可用的因子表达式。"
                "对于生成的表达式，你能够解释其有效性，并且能够用清晰简洁的语言解释其各个变量的含义。\n"
            )
        }, {
            "role": "user",
            "content": (
                f"用户指令描述: {self.user_prompt}\n"
                f"样例数据：{self.sources}\n"
                f"你的任务是学习以上资源之后，总结其规律，输出一个同类型表达式。\n"
                f"书写表达式时，请仅使用样例数据里的函数，每次生成1个，生成的表达式，不要带Alpha#xxx,期望因子的相关性低\n"
                f"Please return nothing but a JSON in the following format:\n"
                f'{{"expr": "生成的因子表达式", "desc": "对该因子表达式的解释说明"}}\n'
            )
        }]
        return prompt

    def run(self):
        lc_messages = convert_openai_messages(self.build_prompt())
        response = self.model.invoke(lc_messages).content
        return json.loads(response)

# Function to stream FactorGPTAgent response
def stream_factor_response(user_prompt):
    factor_agent = FactorGPTAgent(user_prompt)
    response = factor_agent.run()
    response_message = f"因子表达式: {response['expr']}\n\n解释: {response['desc']}"
    logger.info(f"Factor response: {response_message}")
    return response_message

# Main function for Streamlit app
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

    # Prompt for user input and save to chat history
    if prompt := st.chat_input("请描述您的因子分析需求"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        logger.info(f"User input: {prompt}")

        # Display the user's query
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Generate a response based on the user's input
        with st.chat_message("assistant"):
            start_time = time.time()
            logger.info("Generating response")

            with st.spinner("生成中..."):
                try:
                    # Check if the query is related to "因子" (factor)
                    if "因子" in prompt:
                        response_message = stream_factor_response(prompt)
                        st.write(response_message)
                    else:
                        response_message = "这个系统只回答与因子分析相关的问题。"
                        st.write(response_message)
                    
                    duration = time.time() - start_time
                    response_message_with_duration = (
                        f"{response_message}\n\nDuration: {duration:.2f} seconds"
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response_message_with_duration}
                    )
                    logger.info(f"Response: {response_message}, Duration: {duration:.2f} s")
                except Exception as e:
                    st.session_state.messages.append({"role": "assistant", "content": str(e)})
                    st.error("生成响应时发生错误。")
                    logger.error(f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()
