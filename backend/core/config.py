from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    # LLM 配置
    LLM_MODEL_NAME: str
    LLM_API_KEY: str
    LLM_BASE_URL: str
    LLM_TEMPERATURE: float
    LLM_MAX_TOKENS: int
    LLM_STREAMING: bool

    # ASR 配置
    ASR_MODEL_NAME: str
    ASR_API_KEY: str
    ASR_BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()