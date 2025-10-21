from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File
from typing import Dict, Any, List
from src.services.document_service import document_service

# 创建路由器
router = APIRouter()

# 依赖项：获取用户ID
async def get_user_id(x_user_id: str = Header(...)) -> str:
    """从请求头获取用户ID"""
    if not x_user_id:
        raise HTTPException(status_code=400, detail="Missing user ID")
    return x_user_id

@router.post("/upload", response_model=Dict[str, Any])
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Depends(get_user_id)
) -> Dict[str, Any]:
    """
    上传文档
    
    Args:
        file: 要上传的文件（支持pdf、txt、md、csv格式）
        user_id: 用户ID
        
    Returns:
        上传结果
    """
    print('======' * 10)
    try:
        result = await document_service.upload_and_process_document(file, user_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{file_name}", response_model=Dict[str, Any])
async def delete_document(
    file_name: str,
    user_id: str = Depends(get_user_id)
) -> Dict[str, Any]:
    """
    删除文档
    
    Args:
        file_name: 要删除的文件名
        user_id: 用户ID
        
    Returns:
        删除结果
    """
    try:
        result = await document_service.delete_document(user_id, file_name)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Dict[str, Any]])
async def list_documents(
    user_id: str = Depends(get_user_id)
) -> List[Dict[str, Any]]:
    """
    列出用户的所有文档
    
    Args:
        user_id: 用户ID
        
    Returns:
        文档列表
    """
    try:
        documents = await document_service.list_documents(user_id)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))