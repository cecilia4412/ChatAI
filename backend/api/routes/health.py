"""
健康检查路由
"""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ChatAI Backend",
        "version": "0.1.0"
    }


@router.get("/")
async def root():
    """根路径"""
    return {
        "message": "ChatAI Backend API",
        "docs": "/docs",
        "health": "/api/health"
    }
