"""
对话记忆管理
使用 LangChain 的记忆组件管理对话历史
"""

from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from loguru import logger


class ConversationMemory(BaseChatMessageHistory):
    """对话记忆"""
    
    def __init__(self, max_messages: int = 20):
        """
        初始化对话记忆
        
        Args:
            max_messages: 最大保存消息数量
        """
        self.messages: List[BaseMessage] = []
        self.max_messages = max_messages
        logger.info(f"对话记忆初始化: max_messages={max_messages}")
    
    def add_message(self, role: str, content: str):
        """
        添加消息
        
        Args:
            role: 角色 (human/ai/system)
            content: 消息内容
        """
        if role == "human":
            message = HumanMessage(content=content)
        elif role == "ai":
            message = AIMessage(content=content)
        elif role == "system":
            message = SystemMessage(content=content)
        else:
            raise ValueError(f"未知角色: {role}")
        
        self.messages.append(message)
        
        # 限制消息数量
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        
        logger.debug(f"添加消息: {role} - {content[:50]}...")
    
    def add_messages(self, messages: List[BaseMessage]):
        """批量添加消息"""
        self.messages.extend(messages)
        
        # 限制消息数量
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self) -> List[BaseMessage]:
        """获取所有消息"""
        return self.messages
    
    def clear(self):
        """清空消息"""
        self.messages = []
        logger.info("对话记忆已清空")
    
    def get_last_n_messages(self, n: int) -> List[BaseMessage]:
        """获取最后 N 条消息"""
        return self.messages[-n:] if n < len(self.messages) else self.messages
    
    def to_dict(self) -> List[Dict[str, str]]:
        """转换为字典格式"""
        return [
            {
                "role": self._get_role(msg),
                "content": msg.content
            }
            for msg in self.messages
        ]
    
    @staticmethod
    def _get_role(message: BaseMessage) -> str:
        """获取消息角色"""
        if isinstance(message, HumanMessage):
            return "human"
        elif isinstance(message, AIMessage):
            return "ai"
        elif isinstance(message, SystemMessage):
            return "system"
        return "unknown"
    
    def __len__(self) -> int:
        """返回消息数量"""
        return len(self.messages)
    
    def __repr__(self) -> str:
        return f"ConversationMemory(messages={len(self.messages)}, max={self.max_messages})"
