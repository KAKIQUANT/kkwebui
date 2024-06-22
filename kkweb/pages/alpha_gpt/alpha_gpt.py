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

# Define a function to handle chat response generation and streaming
def generate_response(messages):
    try:
        response = client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=messages,
            temperature=0.3,
            stream=True,
        )

        collected_messages = []
        response_placeholder = st.empty()

        for idx, chunk in enumerate(response):
            chunk_message = chunk.choices[0].delta
            if not chunk_message.content:
                continue
            collected_messages.append(chunk_message)
            response_text = ''.join([m.content for m in collected_messages])
            response_placeholder.write(response_text)

        return response_text

    except Exception as e:
        logging.error(f"Error during response generation: {str(e)}")
        raise e

# Function to stream FactorGPTAgent response
def stream_factor_response(user_prompt):
    factor_agent = FactorGPTAgent(user_prompt)
    response = factor_agent.run()
    response_message = f"因子表达式: {response['expr']}\n\n解释: {response['desc']}"
    response_placeholder = st.empty()
    for line in response_message.split('\n'):
        response_placeholder.write(line)
        time.sleep(0.1)
    return response_message

# Main function for Streamlit app
def main():
    st.title("Chat with LLMs Models")
    st.sidebar.write("### General Guidelines")
    st.sidebar.write(
        """
        - Start your query with a clear question or statement.
        - Be specific about what you need.
        - You can ask follow-up questions based on previous answers.
        """
    )

    logger.info("App started")

    # Sidebar for model selection
    model = st.sidebar.selectbox("Choose a model", ["moonshot-v1-8k"])
    logger.info(f"Model selected: {model}")

    # Prompt for user input and save to chat history
    if prompt := st.chat_input("Your question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        logger.info(f"User input: {prompt}")

        # Display the user's query
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Generate a new response if the last message is not from the assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                start_time = time.time()
                logger.info("Generating response")

                with st.spinner("Writing..."):
                    try:
                        # Check if the query is related to "因子" (factor)
                        if "因子" in prompt:
                            response_message = stream_factor_response(prompt)
                        else:
                            # Generate response for the user's input
                            messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
                            system_message = {
                                "role": "system",
                                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
                            }
                            messages.insert(0, system_message)
                            response_message = generate_response(messages)
                        
                        duration = time.time() - start_time
                        response_message_with_duration = (
                            f"{response_message}\n\nDuration: {duration:.2f} seconds"
                        )
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response_message_with_duration}
                        )
                        st.write(f"Duration: {duration:.2f} seconds")
                        logger.info(f"Response: {response_message}, Duration: {duration:.2f} s")

                    except Exception as e:
                        st.session_state.messages.append({"role": "assistant", "content": str(e)})
                        st.error("An error occurred while generating the response.")
                        logger.error(f"Error: {str(e)}")

# Run the app
if __name__ == "__main__":
    main()
