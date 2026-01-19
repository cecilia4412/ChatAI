"""
LLM 基类
定义大语言模型的统一接口（基于 LangChain）
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, List, Dict, Optional
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


class LLMBase(ABC):
    """LLM 基类（LangChain 版本）"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.llm: Optional[BaseChatModel] = None
    
    @abstractmethod
    async def initialize(self):
        """初始化模型"""
        pass
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        context: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        生成回复
        
        Args:
            prompt: 用户输入
            context: 对话上下文
            
        Returns:
            生成的回复
        """
        pass
    
    @abstractmethod
    async def generate_stream(
        self, 
        prompt: str,
        context: Optional[List[Dict[str, str]]] = None
    ) -> AsyncIterator[str]:
        """
        流式生成回复
        
        Args:
            prompt: 用户输入
            context: 对话上下文
            
        Yields:
            逐字生成的回复
        """
        pass
    
    async def cleanup(self):
        """清理资源"""
        pass
