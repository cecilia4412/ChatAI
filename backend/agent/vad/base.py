"""
VAD 基类
定义语音活动检测的统一接口
"""

from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np


class VADBase(ABC):
    """VAD 基类"""
    
    def __init__(
        self, 
        threshold: float = 0.5,
        min_silence_duration: int = 300,
        speech_pad: int = 30
    ):
        self.threshold = threshold
        self.min_silence_duration = min_silence_duration
        self.speech_pad = speech_pad
    
    @abstractmethod
    async def initialize(self):
        """初始化 VAD 模型"""
        pass
    
    @abstractmethod
    async def detect(self, audio_chunk: bytes) -> bool:
        """
        检测音频片段是否包含语音
        
        Args:
            audio_chunk: 音频数据
            
        Returns:
            True 表示检测到语音，False 表示静音
        """
        pass
    
    @abstractmethod
    async def get_speech_timestamps(
        self, 
        audio_data: bytes
    ) -> list[Tuple[int, int]]:
        """
        获取语音片段的时间戳
        
        Args:
            audio_data: 完整音频数据
            
        Returns:
            语音片段的起止时间戳列表 [(start, end), ...]
        """
        pass
    
    async def cleanup(self):
        """清理资源"""
        pass
