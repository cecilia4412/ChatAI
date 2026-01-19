"""
ChatAI Backend - 主入口文件
实时语音通话后端服务
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from core.config.settings import settings
from api.routes import health, websocket

# 配置日志
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL,
)
logger.add(
    "logs/app_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="7 days",
    level="INFO",
)

# 创建 FastAPI 应用
app = FastAPI(
    title="ChatAI Backend API",
    description="实时语音通话后端服务",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(health.router, prefix="/api", tags=["健康检查"])
app.include_router(websocket.router, prefix="/api", tags=["WebSocket"])


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("🚀 ChatAI Backend 正在启动...")
    logger.info(f"📝 环境: {'开发' if settings.DEBUG else '生产'}")
    logger.info(f"🌐 服务地址: http://{settings.HOST}:{settings.PORT}")
    logger.info(f"📚 API 文档: http://{settings.HOST}:{settings.PORT}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("👋 ChatAI Backend 正在关闭...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
