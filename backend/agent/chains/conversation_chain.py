"""
对话链实现
使用 LangChain 构建对话流程
"""

from typing import AsyncIterator, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from loguru import logger

from core.config.settings import settings
from agent.memory.conversation_memory import ConversationMemory


class ConversationChain:
    """对话链"""
    
    def __init__(
        self,
        model_name: str = None,
        temperature: float = 0.7,
        streaming: bool = True
    ):
        """
        初始化对话链
        
        Args:
            model_name: 模型名称
            temperature: 温度参数
            streaming: 是否启用流式输出
        """
        self.model_name = model_name or settings.OPENAI_MODEL
        self.temperature = temperature
        self.streaming = streaming
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            streaming=self.streaming,
            api_key=settings.OPENAI_API_KEY
        )
        
        # 初始化记忆
        self.memory = ConversationMemory()
        
        # 创建提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个友好、专业的 AI 助手，名叫豆包。
你的任务是通过语音与用户进行自然、流畅的对话。

特点：
- 回答简洁明了，适合语音播报
- 语气自然、亲切
- 避免使用过长的句子
- 适当使用口语化表达
- 如果不确定，诚实地说不知道

当前时间：{current_time}
"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 构建链
        self.chain = (
            RunnablePassthrough.assign(
                history=lambda x: self.memory.get_messages()
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        logger.info(f"对话链初始化完成: {self.model_name}")
    
    async def generate(self, user_input: str, **kwargs) -> str:
        """
        生成回复
        
        Args:
            user_input: 用户输入
            **kwargs: 额外参数
            
        Returns:
            AI 回复
        """
        try:
            # 准备输入
            input_data = {
                "input": user_input,
                "current_time": self._get_current_time(),
                **kwargs
            }
            
            # 调用链
            response = await self.chain.ainvoke(input_data)
            
            # 保存到记忆
            self.memory.add_message("human", user_input)
            self.memory.add_message("ai", response)
            
            logger.info(f"生成回复: {response[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"生成回复失败: {e}")
            raise
    
    async def generate_stream(
        self, 
        user_input: str, 
        **kwargs
    ) -> AsyncIterator[str]:
        """
        流式生成回复
        
        Args:
            user_input: 用户输入
            **kwargs: 额外参数
            
        Yields:
            逐字生成的回复
        """
        try:
            # 准备输入
            input_data = {
                "input": user_input,
                "current_time": self._get_current_time(),
                **kwargs
            }
            
            # 流式调用
            full_response = ""
            async for chunk in self.chain.astream(input_data):
                full_response += chunk
                yield chunk
            
            # 保存到记忆
            self.memory.add_message("human", user_input)
            self.memory.add_message("ai", full_response)
            
            logger.info(f"流式生成完成: {full_response[:50]}...")
            
        except Exception as e:
            logger.error(f"流式生成失败: {e}")
            raise
    
    def clear_memory(self):
        """清空对话记忆"""
        self.memory.clear()
        logger.info("对话记忆已清空")
    
    def get_history(self) -> list:
        """获取对话历史"""
        return self.memory.get_messages()
    
    @staticmethod
    def _get_current_time() -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
