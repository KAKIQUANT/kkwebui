from concurrent.futures import ThreadPoolExecutor

from langchain_community.tools.file_management import MoveFileTool
from langchain_core.messages import HumanMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from langgraph.graph import Graph, END
from agents.factor_gpt import FactorGPTAgent
from agents.eval_gpt import EvalGPTAgent
import os

workflow = Graph()
workflow.add_node("factor", FactorGPTAgent().run)
workflow.add_node("eval", EvalGPTAgent().run)
workflow.add_edge('factor', 'eval')
workflow.add_edge('eval', END)

workflow.set_entry_point("factor")

chain = workflow.compile()
chain.invoke({})