from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from src.services.chat_service import chat_service

# 创建路由器
router = APIRouter()

# 定义聊天请求模型
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None
    use_rag: bool = True

# 依赖项：获取用户ID
async def get_user_id(x_user_id: str = Header(...)) -> str:
    """从请求头获取用户ID"""
    if not x_user_id:
        raise HTTPException(status_code=400, detail="Missing user ID")
    return x_user_id

@router.post("/invoke", response_model=Dict[str, Any])
async def send_message_invoke(
    request: ChatRequest,
    user_id: str = Depends(get_user_id)
) -> Dict[str, Any]:
    """
    发送消息给客服
    
    Args:
        request: 聊天请求
        user_id: 用户ID
        
    Returns:
        聊天响应
    """
    try:
        if request.use_rag:
            # 使用RAG功能
            response = await chat_service.chat_with_rag(
                user_id=user_id,
                query=request.message,
                history=request.history
            )
        else:
            # 简单聊天
            response = await chat_service.simple_chat(
                query=request.message,
                history=request.history
            )

        if response["status"] == "error":
            raise HTTPException(status_code=500, detail=response.get("error", "处理请求失败"))

        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream", response_model=Dict[str, Any])
async def send_message_stream(
        request: ChatRequest,
        user_id: str = Depends(get_user_id)
) -> Dict[str, Any]:
    """
    发送消息给客服

    Args:
        request: 聊天请求
        user_id: 用户ID

    Returns:
        聊天响应
    """
    try:
        if request.use_rag:
            # 使用RAG功能
            response = await chat_service.chat_with_rag(
                user_id=user_id,
                query=request.message,
                history=request.history
            )
        else:
            # 简单聊天
            response = await chat_service.simple_chat(
                query=request.message,
                history=request.history
            )

        if response["status"] == "error":
            raise HTTPException(status_code=500, detail=response.get("error", "处理请求失败"))

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))