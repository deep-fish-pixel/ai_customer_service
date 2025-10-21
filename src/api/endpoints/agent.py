from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Dict, Any, List
from pydantic import BaseModel
from src.services.agent_service import agent_service

# 创建路由器
router = APIRouter()

# 定义请求模型
class LeaveRequest(BaseModel):
    request_text: str

class MeetingRequest(BaseModel):
    request_text: str

# 依赖项：获取用户ID
async def get_user_id(x_user_id: str = Header(...)) -> str:
    """从请求头获取用户ID"""
    if not x_user_id:
        raise HTTPException(status_code=400, detail="Missing user ID")
    return x_user_id

@router.post("/leave", response_model=Dict[str, Any])
async def request_leave(
    request: LeaveRequest,
    user_id: str = Depends(get_user_id)
) -> Dict[str, Any]:
    """
    申请请假
    
    Args:
        request: 请假请求
        user_id: 用户ID
        
    Returns:
        处理结果
    """
    try:
        result = await agent_service.process_leave_request(user_id, request.request_text)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result.get("error", "处理请假请求失败"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/meeting", response_model=Dict[str, Any])
async def schedule_meeting(
    request: MeetingRequest,
    user_id: str = Depends(get_user_id)
) -> Dict[str, Any]:
    """
    预约会议
    
    Args:
        request: 会议预约请求
        user_id: 用户ID
        
    Returns:
        处理结果
    """
    try:
        result = await agent_service.process_meeting_request(user_id, request.request_text)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result.get("error", "处理会议预约请求失败"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/leave/records", response_model=List[Dict[str, Any]])
async def get_leave_records(
    user_id: str = Depends(get_user_id)
) -> List[Dict[str, Any]]:
    """
    获取请假记录
    
    Args:
        user_id: 用户ID
        
    Returns:
        请假记录列表
    """
    try:
        records = await agent_service.list_leave_records(user_id)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/meeting/records", response_model=List[Dict[str, Any]])
async def get_meeting_records(
    user_id: str = Depends(get_user_id)
) -> List[Dict[str, Any]]:
    """
    获取会议记录
    
    Args:
        user_id: 用户ID
        
    Returns:
        会议记录列表
    """
    try:
        records = await agent_service.list_meeting_records(user_id)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))