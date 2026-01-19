"""
TTS 基类
定义语音合成的统一接口
"""

from abc import ABC, abstractmethod
from typing import AsyncIterator, Optional


class TTSBase(ABC):
    """TTS 基类"""
    
    def __init__(self, voice: str, rate: str = "+0%", volume: str = "+0%"):
        self.voice = voice
        self.rate = rate
        self.volume = volume
    
    @abstractmethod
    async def initialize(self):
        """初始化 TTS 引擎"""
        pass
    
    @abstractmethod
    async def synthesize(self, text: str) -> bytes:
        """
        合成语音
        
        Args:
            text: 要合成的文本
            
        Returns:
            音频数据（bytes）
        """
        pass
    
    @abstractmethod
    async def synthesize_stream(
        self, 
        text_stream: AsyncIterator[str]
    ) -> AsyncIterator[bytes]:
        """
        流式合成语音
        
        Args:
            text_stream: 文本流
            
        Yields:
            音频数据流
        """
        pass
    
    async def cleanup(self):
        """清理资源"""
        pass
