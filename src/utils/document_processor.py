import os
from typing import List, Dict, Any
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, ToMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import markdown
from bs4 import BeautifulSoup

class DocumentProcessor:
    """文档处理工具类"""
    
    @staticmethod
    def load_document(file_path: str) -> List[Dict[str, Any]]:
        """
        加载不同格式的文档
        
        Args:
            file_path: 文件路径
            
        Returns:
            文档内容列表
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            elif file_ext == '.txt':
                loader = TextLoader(file_path, encoding='utf-8')
                documents = loader.load()
            elif file_ext == '.csv':
                loader = CSVLoader(file_path, encoding='utf-8')
                documents = loader.load()
            elif file_ext == '.md':
                # 处理Markdown文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                # 将Markdown转换为纯文本
                html = markdown.markdown(md_content)
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
                documents = [
                    Document(page_content=text, metadata={"source": file_path}),
                ]
            else:
                raise ValueError(f"不支持的文件格式: {file_ext}")
            
            return documents
        except Exception as e:
            print(f"加载文档失败: {e}")
            raise
    
    @staticmethod
    def split_documents(documents: List[Dict[str, Any]], chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Dict[str, Any]]:
        """
        切分文档为小块
        
        Args:
            documents: 文档内容列表
            chunk_size: 每块的大小
            chunk_overlap: 块之间的重叠大小
            
        Returns:
            切分后的文档块列表
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        return chunks
    
    @staticmethod
    def get_document_metadata(file_path: str) -> Dict[str, Any]:
        """
        获取文档元数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            文档元数据
        """
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1].lower()
        file_size = os.path.getsize(file_path)
        
        return {
            "file_name": file_name,
            "file_extension": file_ext,
            "file_size": file_size,
            "file_path": file_path
        }