import os
from typing import Dict, Any, List, Optional, Literal
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Optional


from src import RESPONSE_STATUS_FAILED, RESPONSE_STATUS_SUCCESS
from src.services.graphs import get_task_graph, SUPPORTED_TASKS
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
            temperature=0
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
            return context
        except Exception as e:
            print(f"获取RAG上下文失败: {e}")
            return []
    
    def classify_task(self, query: str) -> Dict[str, str]:
        """将用户查询分类为支持的任务类型"""
        prompt_template = ChatPromptTemplate.from_template("""
        你是任务分类器。分析用户查询并将其分类为以下任务类型之一: {supported_tasks}。
        
        要求：
            严格匹配，没有完整的信息匹配则算不匹配，如果不匹配，返回empty。
                实例1：
                    我想出去玩
                    没有跟定机票或定酒店直接相关，故不需要匹配。
                实例2：
                    如何定机票？
                    他只是在询问，没有让你定机票，故不需要匹配。
                实例3：
                    我想定个明天的机票
                    有跟定机票相关，故需要匹配。
            只返回确切的任务类型字符串，不包含任何额外文本、解释或标点符号。
        
        用户查询: {query}
        """
        )

        chain = prompt_template | self.llm | StrOutputParser()
        task_type = chain.invoke({
            "supported_tasks": ", ".join(SUPPORTED_TASKS),
            "query": query
        }).strip()

        # 如果分类不明确则返回默认值
        # return task_type if task_type in SUPPORTED_TASKS else "general_chat"
        if task_type in SUPPORTED_TASKS:
            return {
                "task_type": task_type,
                "question": "",
            }
        else:
            return {
                "task_type": '',
                "question": task_type if task_type == '' else task_type
            }

    async def process_with_langgraph(
        self,
        user_id: str,
        query: str,
        history: Optional[List[Dict[str, str]]] = None,
        task_type: str = '',
        task_extra: Dict[str, str] = None,
    ) -> Any:
        """使用LangGraph处理特定任务"""
        graph = get_task_graph(task_type)

        input_data = {
            "task_status": 0,
            "user_id": user_id,
            "query": query,
            "task_type":task_type,
            "task_extra": task_extra,
            "history": history or [],
            "exit": 0,
        }

        app = graph.compile()
        # result = await app.ainvoke(input_data)
        # {'collect_info': {'query': '请提供您的出发城市、目的地和出行日期，我将为您预订航班。'}}
        return app.astream(
            input_data,
            # {"recursion_limit": 50},
            stream_mode="values"
        )

    async def chat_with_rag(self, user_id: str, query: str, history: List[Dict[str, str]] = None, task_type: str = '', task_extra: Dict[str, str] = None, stream: bool = False) -> Any:
        """
        使用RAG进行聊天

        Args:
            user_id: 用户ID
            query: 用户查询
            history: 聊天历史
            stream: 是否流式返回

        Returns:
            聊天响应
        """
        try:

            if task_type == '':
                # 获取RAG上下文
                context = self.get_rag_context(user_id, query)

                # 任务分类与路由
                task = self.classify_task(query)

                task_type = task['task_type']

                question = task['question']

                if question != '' and question != 'empty':
                   return question

            if task_type in SUPPORTED_TASKS:
                # 使用langgraph处理特定任务
                result = await self.process_with_langgraph(user_id, query, history, task_type, task_extra)
                return result


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
                history_text = "\n".join([f"{item['sender']}: {item['content']}" for item in history])

            # 格式化上下文
            context_text = "\n\n".join(context)

            # 创建链式调用
            chain = prompt_template | self.llm | self.output_parser

            if stream:
                # 流式响应
                return chain.stream({
                    "context": context_text,
                    "history": history_text,
                    "query": query
                })
            else:
                # 执行链式调用
                response = chain.invoke({
                    "context": context_text,
                    "history": history_text,
                    "query": query
                })

                return {
                    "status": RESPONSE_STATUS_SUCCESS,
                    "data": response,
                    "has_context": len(context) > 0
                }

        except Exception as e:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"处理请求失败: {str(e)}"
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
            history_text = "\n".join([f"{item['sender']}: {item['content']}" for item in history])
        
        # 创建链式调用
        chain = prompt_template | self.llm | self.output_parser
        
        try:
            # 执行链式调用
            response = chain.invoke({
                "history": history_text,
                "query": query
            })
            
            return {
                "status": RESPONSE_STATUS_SUCCESS,
                "data": response
            }
            
        except Exception as e:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"处理请求失败: {str(e)}"
            }

# 创建全局聊天服务实例
chat_service = ChatService()