from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from src.services.graphs.agent_state import AgentState
from src.services.relative_db_service import relative_db_service
from typing import Optional


class HotelBookingInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0


def query_hotel_booking_graph() -> StateGraph:
    """查询宾馆预订的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息提取和验证函数
    async def query(state: AgentState) -> AgentState:
        result = relative_db_service.list_hotel_bookings(state['user_id'])

        query = '已查询到您的宾馆预定如下：'

        for booking_info in result:
            query += f"""\n
            [id:{booking_info["id"]}  城市:{booking_info["city"]} 入住日期:{booking_info["checkin_date"]} 退房日期:{booking_info["checkout_date"]} 房型:{booking_info["room_type"]} 人数:{booking_info["guest_count"]}]"""

        return {** state, "task_response": 2, "query": query}

    # 添加节点到图中
    graph.add_node("query", query)
    # 设置图的入口点
    graph.set_entry_point("query")
    graph.add_edge("query", END)


    return graph