"""
ASR 基类
定义语音识别的统一接口
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional
import numpy as np


class ASRBase(ABC):
    """ASR 基类"""
    
    def __init__(self, model_name: str, language: str = "zh"):
        self.model_name = model_name
        self.language = language
        self.model = None
    
    @abstractmethod
    async def initialize(self):
        """初始化模型"""
        pass
    
    @abstractmethod
    async def transcribe(self, audio_data: bytes) -> str:
        """
        转录音频为文本
        
        Args:
            audio_data: 音频数据（bytes）
            
        Returns:
            转录文本
        """
        pass
    
    @abstractmethod
    async def transcribe_stream(
        self, 
        audio_stream: AsyncIterator[bytes]
    ) -> AsyncIterator[str]:
        """
        流式转录
        
        Args:
            audio_stream: 音频流
            
        Yields:
            实时转录文本
        """
        pass
    
    async def cleanup(self):
        """清理资源"""
        pass
