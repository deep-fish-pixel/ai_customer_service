import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.services.vector_db_service import vector_db_service
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ChatService:
    """聊天服务类"""
    
    def __init__(self):
        """初始化聊天服务"""
        self.llm = ChatOpenAI(
            # api_key=os.getenv("OPENAI_API_KEY"),
            # model_name="gpt-3.5-turbo",
            model="qwen-max",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("API_BASE_URL"),
            temperature=0.7
        )
        self.output_parser = StrOutputParser()
    
    def get_rag_context(self, user_id: str, query: str, k: int = 3) -> List[str]:
        """
        获取RAG上下文
        
        Args:
            user_id: 用户ID
            query: 查询内容
            k: 返回的文档数量
            
        Returns:
            上下文文本列表
        """
        collection_name = f"user_{user_id}_documents"
        try:
            # 搜索相似文档
            similar_docs = vector_db_service.similarity_search(collection_name, query, k=k)
            # 提取文档内容
            context = [doc.page_content for doc in similar_docs]
            print(context[0] == context[1])
            return context
        except Exception as e:
            print(f"获取RAG上下文失败: {e}")
            return []
    
    async def chat_with_rag(self, user_id: str, query: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        使用RAG进行聊天
        
        Args:
            user_id: 用户ID
            query: 用户查询
            history: 聊天历史
            
        Returns:
            聊天响应
        """
        # 获取RAG上下文
        context = self.get_rag_context(user_id, query)
        
        # 构建提示模板
        prompt_template = ChatPromptTemplate.from_template("""
        你是小智，一个智能客服助手。请基于以下上下文信息回答用户的问题。
        
        上下文信息:
        {context}
        
        聊天历史:
        {history}
        
        用户的问题:
        {query}
        
        请以友好、专业的语气回答用户的问题。如果上下文信息中没有相关内容，
        请直接回答用户，不要提及上下文。
        """)
        
        # 格式化聊天历史
        history_text = ""
        if history:
            history_text = "\n".join([f"{item['role']}: {item['content']}" for item in history])
        
        # 格式化上下文
        context_text = "\n\n".join(context)
        
        # 创建链式调用
        chain = prompt_template | self.llm | self.output_parser
        
        try:
            # 执行链式调用
            response = chain.invoke({
                "context": context_text,
                "history": history_text,
                "query": query
            })
            
            return {
                "status": "success",
                "response": response,
                "has_context": len(context) > 0
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"处理请求失败: {str(e)}"
            }
    
    async def simple_chat(self, query: str, history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        简单聊天（不使用RAG）
        
        Args:
            query: 用户查询
            history: 聊天历史
            
        Returns:
            聊天响应
        """
        # 构建提示模板
        prompt_template = ChatPromptTemplate.from_template("""
        你是小智，一个智能客服助手。请以友好、专业的语气回答用户的问题。
        
        聊天历史:
        {history}
        
        用户的问题:
        {query}
        """)
        
        # 格式化聊天历史
        history_text = ""
        if history:
            history_text = "\n".join([f"{item['role']}: {item['content']}" for item in history])
        
        # 创建链式调用
        chain = prompt_template | self.llm | self.output_parser
        
        try:
            # 执行链式调用
            response = chain.invoke({
                "history": history_text,
                "query": query
            })
            
            return {
                "status": "success",
                "response": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"处理请求失败: {str(e)}"
            }

# 创建全局聊天服务实例
chat_service = ChatService()