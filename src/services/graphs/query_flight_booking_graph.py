from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getHistoryAndNextQuestion
from src.services.relative_db_service import relative_db_service
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional
from src.utils.getOpenAI import getChatOpenAI


class FlightBookingInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0


def query_flight_booking_graph() -> StateGraph:
    """查询航班预订的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息提取和验证函数
    async def query(state: AgentState) -> AgentState:
        result = relative_db_service.list_flight_bookings(state['user_id'])

        query = '已查询到您的机票预定如下：'

        for booking_info in result:
            query += f"""\n
            [id:{booking_info["id"]}  始发地:{booking_info["origin"]} 目的地:{booking_info["destination"]}时间:{booking_info["date"]} 座位等级:{booking_info["seat_class"]} 座位偏好:{booking_info["seat_preference"]}]"""

        return {** state, "task_response": 2, "query": query}

    # 添加节点到图中
    graph.add_node("query", query)
    # 设置图的入口点
    graph.set_entry_point("query")
    graph.add_edge("query", END)


    return graph