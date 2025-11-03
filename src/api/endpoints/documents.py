from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File
from typing import Dict, Any, List

from src import RESPONSE_STATUS_SUCCESS, Response
from src.services.document_service import document_service
from src.api.endpoints import get_user_id

# 创建路由器
router = APIRouter()

@router.post("/upload", response_model=Response)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Depends(get_user_id)
) -> Response:
    """
    上传文档
    
    Args:
        file: 要上传的文件（支持pdf、txt、md、csv格式）
        user_id: 用户ID
        
    Returns:
        上传结果
    """
    try:
        result = await document_service.upload_and_process_document(file, user_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{file_name}", response_model=Response)
async def delete_document(
    file_name: str,
    user_id: str = Depends(get_user_id)
) -> Response:
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

@router.get("/", response_model=Response)
async def list_documents(
    user_id: str = Depends(get_user_id)
) -> Response:
    """
    列出用户的所有文档
    
    Args:
        space_id: 用户ID
        
    Returns:
        Response
    """
    try:
        documents = await document_service.list_documents(space_id)
        return {
          "status": RESPONSE_STATUS_SUCCESS,
          "message":"",
          "response": documents,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))