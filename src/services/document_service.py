import os
from typing import List, Dict, Any, Coroutine
from fastapi import UploadFile, HTTPException

from src import RESPONSE_STATUS_SUCCESS, Response, RESPONSE_STATUS_FAILED
from src.utils.document_processor import DocumentProcessor
from src.services.vector_db_service import vector_db_service
from src.services.relative_db_service import relative_db_service
from dotenv import load_dotenv
import datetime

# 加载环境变量
load_dotenv()

class DocumentService:
    """文档服务类"""
    
    def __init__(self):
        """初始化文档服务"""
        self.upload_dir = os.getenv("UPLOAD_DIR", "./uploads")
        self.document_processor = DocumentProcessor()
        # 确保上传目录存在
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_uploaded_file(self, user_id: str, file: UploadFile) -> dict[str, str | None] | str:
        """
        保存上传的文件
        
        Args:
            file: 上传的文件
            
        Returns:
            文件路径
        """
        # 检查文件格式
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.pdf', '.txt', '.md', '.csv']:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"不支持的文件格式: {file_ext}",
                "response": None
            }
        
        # 保存文件
        # 确保用户特定的上传目录存在
        user_upload_dir = os.path.join(self.upload_dir, user_id)
        os.makedirs(user_upload_dir, exist_ok=True)
        
        file_path = os.path.join(user_upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path
    
    async def upload_and_process_document(self, file: UploadFile, user_id: str) -> Response:
        """
        上传并处理文档
        
        Args:
            file: 上传的文件
            user_id: 用户ID
            
        Returns:
            处理结果
        """
        try:
            document_info = relative_db_service.get_document_info(user_id, file.filename)

            if (document_info != None):
                return {
                    "status": "failed",
                    "message": "文档已上传过",
                    "response": document_info
                }
            # 保存文件
            file_path = await self.save_uploaded_file(user_id, file)
            
            # 获取文档元数据
            metadata = self.document_processor.get_document_metadata(file_path)
            
            # 加载文档
            documents = self.document_processor.load_document(file_path)
            
            # 切分文档
            chunks = self.document_processor.split_documents(documents)
            
            # 为每个文档块添加用户ID和文档信息
            for chunk in chunks:
                chunk.metadata["user_id"] = user_id
                chunk.metadata["document_name"] = file.filename
            
            # 存储到向量数据库
            collection_name = f"user_{user_id}_documents"
            document_ids = vector_db_service.add_documents(collection_name, chunks)

            # 保存文档信息
            document_info = {
                "file_name": file.filename,
                "file_path": file_path,
                "file_size": metadata["file_size"],
                "document_ids": document_ids,
                "chunks_count": len(chunks),
                "upload_time": datetime.datetime.now()
            }
            
            # 存储文档信息到数据库
            relative_db_service.save_document_info(user_id, document_info)
            
            return {
                "status": RESPONSE_STATUS_SUCCESS,
                "message": "文档上传成功",
                "response": document_info
            }
            
        except Exception as e:
            # 如果处理失败，删除已上传的文件
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"文档处理失败: {str(e)}",
                "response": None
            }
    
    async def delete_document(self, user_id: str, file_name: str) -> Response:
        """
        删除文档
        
        Args:
            user_id: 用户ID
            file_name: 文件名
            
        Returns:
            删除结果
        """
        # 从数据库获取文档信息
        document_info = relative_db_service.get_document_info(user_id, file_name)
        
        if not document_info:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "文档不存在",
                "response": None
            }
        
        try:
            # 从向量数据库删除
            collection_name = f"user_{user_id}_documents"
            vector_db_service.delete_documents(collection_name, document_info["document_ids"])
            
            # 删除本地文件
            if os.path.exists(document_info["file_path"]):
                os.remove(document_info["file_path"])
            
            # 从数据库删除文档信息
            relative_db_service.delete_document_info(user_id, file_name)
            
            return {
                "status": RESPONSE_STATUS_SUCCESS,
                "message": "文档删除成功",
                "response": document_info['file_path']
            }
            
        except Exception as e:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"文档删除失败: {str(e)}",
                "response": None
            }

    async def list_documents(self, user_id: str) -> List[Dict[str, Any]]:
        """
        列出用户的所有文档
        
        Args:
            space_id: 用户ID
            
        Returns:
            文档列表
        """
        # 从数据库获取用户文档列表
        return relative_db_service.list_space_documents(space_id)

# 创建全局文档服务实例
document_service = DocumentService()