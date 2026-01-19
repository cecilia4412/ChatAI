"""
基于 LangChain 的 LLM 实现
支持多种 LLM 提供商（OpenAI、Anthropic 等）
"""

from typing import AsyncIterator, List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from loguru import logger

from .base import LLMBase
from core.config.settings import settings


class LangChainLLM(LLMBase):
    """LangChain LLM 实现"""
    
    def __init__(
        self,
        model_name: str = None,
        temperature: float = 0.7,
        streaming: bool = True,
        max_tokens: int = 2000
    ):
        """
        初始化 LangChain LLM
        
        Args:
            model_name: 模型名称
            temperature: 温度参数
            streaming: 是否启用流式输出
            max_tokens: 最大 token 数
        """
        super().__init__(model_name or settings.OPENAI_MODEL)
        self.temperature = temperature
        self.streaming = streaming
        self.max_tokens = max_tokens
    
    async def initialize(self):
        """初始化 LLM"""
        try:
            self.llm = ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                streaming=self.streaming,
                max_tokens=self.max_tokens,
                api_key=settings.OPENAI_API_KEY
            )
            logger.info(f"LangChain LLM 初始化成功: {self.model_name}")
        except Exception as e:
            logger.error(f"LLM 初始化失败: {e}")
            raise
    
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
        try:
            # 构建消息列表
            messages = self._build_messages(prompt, context)
            
            # 调用 LLM
            response = await self.llm.ainvoke(messages)
            
            logger.info(f"生成回复: {response.content[:50]}...")
            return response.content
            
        except Exception as e:
            logger.error(f"生成回复失败: {e}")
            raise
    
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
        try:
            # 构建消息列表
            messages = self._build_messages(prompt, context)
            
            # 流式调用
            async for chunk in self.llm.astream(messages):
                if chunk.content:
                    yield chunk.content
            
            logger.info("流式生成完成")
            
        except Exception as e:
            logger.error(f"流式生成失败: {e}")
            raise
    
    def _build_messages(
        self, 
        prompt: str, 
        context: Optional[List[Dict[str, str]]] = None
    ) -> List:
        """
        构建消息列表
        
        Args:
            prompt: 用户输入
            context: 对话上下文
            
        Returns:
            消息列表
        """
        messages = []
        
        # 添加系统提示
        messages.append(SystemMessage(content=self._get_system_prompt()))
        
        # 添加历史对话
        if context:
            for msg in context:
                role = msg.get("role", "")
                content = msg.get("content", "")
                
                if role == "human" or role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "ai" or role == "assistant":
                    messages.append(AIMessage(content=content))
        
        # 添加当前输入
        messages.append(HumanMessage(content=prompt))
        
        return messages
    
    @staticmethod
    def _get_system_prompt() -> str:
        """获取系统提示词"""
        from datetime import datetime
        from agent.prompts import VOICE_ASSISTANT_PROMPT
        
        return VOICE_ASSISTANT_PROMPT.format(
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
