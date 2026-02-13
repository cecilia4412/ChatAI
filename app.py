from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="ChatAI API",
    version="1.0.0",
    description="AI语音对话助手API"
)

_chat_service = None


def get_chat_service():
    global _chat_service
    if _chat_service is None:
        from chat_service import ChatService
        _chat_service = ChatService()
    return _chat_service


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    stream: Optional[bool] = False
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    history: List[Message]


@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "ChatAI API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        chat_service = get_chat_service()
        response, updated_history = await chat_service.chat(
            message=request.message,
            history=request.history if request.history else None,
            session_id=request.session_id
        )
        
        return ChatResponse(
            response=response,
            history=updated_history
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"聊天处理失败: {str(e)}")


@app.post("/clear")
async def clear_history(session_id: str = "default"):
    chat_service = get_chat_service()
    chat_service.clear_memory(session_id)
    return {"status": "ok", "message": f"会话 {session_id} 的对话历史已清空"}