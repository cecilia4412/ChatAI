"""
WebSocket 路由
处理实时音频流通信
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from loguru import logger

router = APIRouter()


@router.websocket("/ws/audio")
async def websocket_audio(websocket: WebSocket):
    """
    WebSocket 音频流处理
    
    客户端发送音频数据，服务端返回处理结果
    """
    await websocket.accept()
    logger.info(f"WebSocket 连接建立: {websocket.client}")
    
    try:
        while True:
            # 接收音频数据
            data = await websocket.receive_bytes()
            logger.debug(f"收到音频数据: {len(data)} bytes")
            
            # TODO: 处理音频数据
            # 1. VAD 检测
            # 2. ASR 识别
            # 3. LLM 生成
            # 4. TTS 合成
            
            # 临时响应
            await websocket.send_json({
                "type": "transcript",
                "text": "收到音频数据",
                "timestamp": "2024-01-01T00:00:00"
            })
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket 连接断开: {websocket.client}")
    except Exception as e:
        logger.error(f"WebSocket 错误: {e}")
        await websocket.close()
