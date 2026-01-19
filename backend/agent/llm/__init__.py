"""
LLM (Large Language Model) 模块
大语言模型对话功能（基于 LangChain）
"""

from .base import LLMBase
from .langchain_llm import LangChainLLM

__all__ = ["LLMBase", "LangChainLLM"]
