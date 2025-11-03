from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import StreamingResponse
import asyncio
from typing import AsyncGenerator
from typing import Dict, Any, List, Optional, TypedDict

from src import RESPONSE_STATUS_FAILED
from src.api.endpoints import get_user_id


class ChatMessage(TypedDict):
    sender: str
    content: str
from pydantic import BaseModel
from src.services.chat_service import chat_service

# 创建路由器
router = APIRouter()

# 定义聊天请求模型
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None
    use_rag: bool = True

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

        if response["status"] == RESPONSE_STATUS_FAILED:
            raise HTTPException(status_code=500, detail=response.get(RESPONSE_STATUS_FAILED, "处理请求失败"))

        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 模拟链式流式生成器
async def mock_chain_stream(query: str):
    """模拟流式响应生成器"""
    responses = [
        f"思考中...",
        f"思考中...",
        f"思考中...",
        f"思考中...",
        f"正在处理你的问题: {query}",
        "生成最终回答..."
    ]

    for response in responses:
        yield response
        await asyncio.sleep(0.5)  # 模拟处理延迟



async def stream_generator(request: ChatRequest,
                           user_id: str = Depends(get_user_id), ) -> AsyncGenerator[str, None]:
    """处理流式生成器"""
    try:
        # 在线程池中运行同步的chat_with_rag，避免阻塞事件循环
        result = await chat_service.chat_with_rag(
            user_id=user_id,
            query=request.message,
            history=request.history or [],
            stream=True
        )

        # 检查结果类型
        if isinstance(result, dict):
            # 如果是错误响应或普通响应
            if result.get('status') == RESPONSE_STATUS_FAILED:
                yield result.get(RESPONSE_STATUS_FAILED, '处理请求失败')
            else:
                yield result.get('response', '')
        elif hasattr(result, '__aiter__'):
            # 处理异步迭代器
            async for chunk in result:
                if hasattr(chunk, 'content'):
                    yield str(chunk.content)
                else:
                    yield str(chunk)
        elif hasattr(result, '__iter__') and not isinstance(result, str):
            # 处理同步迭代器，使用线程池避免阻塞事件循环
            loop = asyncio.get_event_loop()
            iterator = iter(result)
            while True:
                try:
                    # 在线程池中获取下一个元素
                    chunk = await loop.run_in_executor(None, lambda: next(iterator, None))
                    if chunk is None:
                        # 迭代结束，正常退出循环
                        break
                    if hasattr(chunk, 'content'):
                        yield str(chunk.content)
                    else:
                        yield str(chunk)
                except StopIteration:
                    # 即使捕获到StopIteration也正常退出
                    break
                except Exception as inner_e:
                    # 捕获其他可能的异常
                    print(f"处理迭代元素时发生错误: {str(inner_e)}")
                    yield f"错误: 处理数据时发生错误"
                    break
        else:
            # 直接返回结果
            yield str(result)
    except Exception as e:
        yield f"错误: {str(e)}"

@router.post("/stream")
async def send_message_stream(
        request: ChatRequest,
        user_id: str = Depends(get_user_id),
        stream: bool = False
):
    """
    发送消息给客服

    Args:
        request: 聊天请求
        user_id: 用户ID
        stream: 是否启用流式响应

    Returns:
        聊天响应或流式响应
    """
    try:
        if request.use_rag:
            if stream:
                async def event_generator():
                    async for chunk in stream_generator(request, user_id):
                        if chunk:
                            # 发送数据块，格式符合Server-Sent Events
                            yield f"data: {chunk}\n\n"
                return StreamingResponse(
                    event_generator(),
                    # media_type="text/event-stream"
                    media_type="text/event-stream"
                )
            else:
                # 普通响应处理
                response = await chat_service.chat_with_rag(
                    user_id=space_id,
                    query=request.message,
                    history=request.history
                )
        else:
            # 简单聊天（非RAG）
            response = await chat_service.simple_chat(
                query=request.message,
                history=request.history
            )

        if isinstance(response, dict) and response["status"] == RESPONSE_STATUS_FAILED:
            raise HTTPException(status_code=500, detail=response.get(RESPONSE_STATUS_FAILED, "处理请求失败"))

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))