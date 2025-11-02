# endpoints包初始化文件
from fastapi import HTTPException, Header

# 依赖项：获取用户ID
async def get_user_id(x_user_id: str = Header(...)) -> str:
    """从请求头获取用户ID"""
    if not x_user_id:
        raise HTTPException(status_code=400, detail="Missing user ID")
    return x_user_id