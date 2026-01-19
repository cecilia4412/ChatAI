"""
配置管理模块
使用 pydantic-settings 管理环境变量
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    
    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # CORS 配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "exp://localhost:8081"]
    
    # OpenAI 配置
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # ASR 配置
    ASR_MODEL: str = "whisper"
    ASR_MODEL_SIZE: str = "base"
    ASR_LANGUAGE: str = "zh"
    
    # TTS 配置
    TTS_ENGINE: str = "edge-tts"
    TTS_VOICE: str = "zh-CN-XiaoxiaoNeural"
    TTS_RATE: str = "+0%"
    TTS_VOLUME: str = "+0%"
    
    # VAD 配置
    VAD_THRESHOLD: float = 0.5
    VAD_MIN_SILENCE_DURATION: int = 300
    VAD_SPEECH_PAD: int = 30
    
    # 音频配置
    AUDIO_SAMPLE_RATE: int = 16000
    AUDIO_CHANNELS: int = 1
    AUDIO_FORMAT: str = "wav"
    
    # 性能配置
    MAX_CONCURRENT_REQUESTS: int = 10
    REQUEST_TIMEOUT: int = 30
    STREAM_BUFFER_SIZE: int = 4096
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
