# encoding:utf-8
import os

from langchain_community.adapters.openai import convert_openai_messages


def read_file_2_list(filepath):
    filepath = os.path.dirname(os.path.realpath(__file__)) + "\\" +filepath
    print(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.readlines()
    return text


sample_json = """
{
  "expr": 生成的因子表达式,
  "desc": 对该因子表达式的解释说明
}
"""

from langchain_openai import ChatOpenAI
import json as json

KEY = ''
if 'OPENAI_API_KEY' in os.environ:
    KEY = os.environ['OPENAI_API_KEY']
    print('{}'.format(KEY))
class FactorGPTAgent:
    def __init__(self):
        self.sources = [x.strip() for x in read_file_2_list('worldquant_101.txt')]
        optional_params = {
            "response_format": {"type": "json_object"}
        }
        # openai_api_key = KIMI_KEY
        self.model = ChatOpenAI(temperature=0, openai_api_key=KEY.strip(), model='moonshot-v1-8k',
                                base_url="https://api.moonshot.cn/v1", max_retries=1, model_kwargs=optional_params)

    def build_prompt(self):
        prompt = [{
            "role": "system",
            "content": "你是一个量化分析师. 你可以通过阅读多个alpha因子表达式，总结其内在规律，并且可以创新性的生成可用的因子表达式。"
                       "对于生成的表达式，你能够解释其有效性，并且能够用清晰简洁的语言解释其各个变量的含义。\n "
        }, {
            "role": "user",
            "content": f"指令描述: 生成因子表达式"
                       f"样例数据：{self.sources}\n"
                       f"你的任务学习以上资源之后，总结其规律，输出一个同类型表达式。\n "
                       f"书写表达式时，请仅使用样例数据里的函数，每次生成1个，,生成的表达式，不要带Alpha#xxx,期望因子的相关性低\n"
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_json}\n "
        }]
        return prompt

    def run(self, info: dict):
        lc_messages = convert_openai_messages(self.build_prompt())
        response = self.model.invoke(
            lc_messages).content
        print(response)
        return json.loads(response)


if __name__ == '__main__':
    FactorGPTAgent().run({})
