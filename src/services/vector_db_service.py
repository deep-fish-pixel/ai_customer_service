import os
from typing import List, Dict, Any, Optional
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class VectorDBService:
    """向量数据库服务类"""
    
    def __init__(self):
        """初始化向量数据库服务"""
        # self.embeddings = OpenAIEmbeddings(
        #     api_key=os.getenv("OPENAI_API_KEY")
        # )
        # 阿里云只支持DashScopeEmbeddings： https://blog.csdn.net/bigcarp/article/details/146334975
        self.embeddings = DashScopeEmbeddings(
            model="text-embedding-v3",
            dashscope_api_key=os.getenv("DASHSCOPE_API_KEY")
        )
        self.db_path = os.getenv("CHROMA_DB_PATH", "./chromadb")
        self.collections: Dict[str, Chroma] = {}
    
    def get_or_create_collection(self, collection_name: str) -> Chroma:
        """
        获取或创建集合
        
        Args:
            collection_name: 集合名称
            
        Returns:
            Chroma集合实例
        """
        if collection_name not in self.collections:
            self.collections[collection_name] = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                persist_directory=os.path.join(self.db_path, collection_name)
            )
        return self.collections[collection_name]
    
    def add_documents(self, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """
        向集合中添加文档
        
        Args:
            collection_name: 集合名称
            documents: 文档列表
            
        Returns:
            添加的文档ID列表
        """
        collection = self.get_or_create_collection(collection_name)
        return collection.add_documents(documents)
    
    def similarity_search(self, collection_name: str, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        相似性搜索
        
        Args:
            collection_name: 集合名称
            query: 搜索查询
            k: 返回的结果数量
            
        Returns:
            搜索结果列表
        """
        collection = self.get_or_create_collection(collection_name)
        return collection.similarity_search(query, k=k)
    
    def delete_documents(self, collection_name: str, document_ids: List[str]) -> None:
        """
        删除文档
        
        Args:
            collection_name: 集合名称
            document_ids: 文档ID列表
        """
        if collection_name in self.collections:
            collection = self.collections[collection_name]
            collection.delete(ids=document_ids)
    
    def delete_collection(self, collection_name: str) -> None:
        """
        删除整个集合
        
        Args:
            collection_name: 集合名称
        """
        if collection_name in self.collections:
            # 这里简化处理，实际可能需要清理持久化目录
            del self.collections[collection_name]
    
    def get_document_ids_by_source(self, collection_name: str, source: str) -> List[str]:
        """
        根据源获取文档ID
        
        Args:
            collection_name: 集合名称
            source: 文档源路径
            
        Returns:
            文档ID列表
        """
        if collection_name not in self.collections:
            return []
        
        collection = self.collections[collection_name]
        # 这里简化处理，实际可能需要查询元数据
        # 在实际使用中，可能需要更复杂的查询逻辑
        return []

# 创建全局向量数据库服务实例
vector_db_service = VectorDBService()