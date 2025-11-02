# endpoints包初始化文件
from fastapi import HTTPException, Header

# 依赖项：获取空间ID
async def get_space_id(x_space_id: str = Header(...)) -> str:
    """从请求头获取空间ID"""
    if not x_space_id:
        raise HTTPException(status_code=400, detail="Missing space ID")
    return x_space_id