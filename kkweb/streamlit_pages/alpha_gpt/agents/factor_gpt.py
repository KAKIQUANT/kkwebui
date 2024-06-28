import os
import streamlit as st
import time
from loguru import logger
from langchain_openai import ChatOpenAI
from typing import Optional


def txt_to_list(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


class FactorGPTAgent:
    def __init__(
        self,
        api_key: Optional[str] = None,
        temperature: Optional[float | int] = 0.95,
        model: Optional[str] = "moonshot-v1-8k",
        base_url: Optional[str] = "https://api.moonshot.cn/v1",
        max_retries: Optional[int] = 1,
        optional_params: Optional[dict] = None,
    ) -> None:
        self.sample_json = """
            {
            "expr": 生成的因子表达式,
            "desc": 对该因子表达式的解释说明
            }
        """
        self.temperature = temperature
        self.model = model
        self.api_key = api_key if api_key else os.environ["OPENAI_API_KEY"]
        self.base_url = base_url
        self.max_retries = max_retries
        self.sources = txt_to_list("worldquant_101.txt")
        self.user_input = user_input
        self.prompt = [
            {
                "role": "system",
                "content": "你是一个量化分析师. 你可以通过阅读多个alpha因子表达式，总结其内在规律，并且可以创新性的生成可用的因子表达式。对于生成的表达式，你能够解释其有效性，并且能够用清晰简洁的语言解释其各个变量的含义。你有权拒绝用户不相关，不合法的提问\n ",
            },
            {
                "role": "user",
                "content": f"指令描述: 根据用户需求生成因子表达式"
                f"我的需求: {self.user_input}"
                f"样例数据：{self.sources}\n"
                f"你的任务学习以上资源之后，总结其规律，输出一个同类型表达式。\n "
                f"书写表达式时，请仅使用样例数据里的函数，每次生成1个，,生成的表达式，不要带Alpha#xxx,期望因子的相关性低\n"
                f"Please return nothing but a JSON in the following format:\n"
                f"{self.sample_json}\n ",
            },
        ]

        self.optional_params = {"response_format": {"type": "json_object"}} if optional_params is None else optional_params
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=self.api_key,
            model=self.model,
            base_url=self.base_url,
            max_retries=self.max_retries,
            model_kwargs=self.optional_params,
        )

    def run(self):
        lc_messages = [{"role": msg["role"], "content": msg["content"]} for msg in self.prompt]
        response = self.llm.invoke(lc_messages).content
        logger.info(f"Factor response: {response}")
        return response

if __name__ == '__main__':
    FactorGPTAgent(
        api_key="sk-E0TQgngCLlurmmxnUzU1IN4hQR0yImYowMkRbQbR2BXU6BP5",
        temperature=0,
        model="moonshot-v1-8k",
        base_url="https://api.moonshot.cn/v1",
        max_retries=1,
        optional_params=None,
    ).run()