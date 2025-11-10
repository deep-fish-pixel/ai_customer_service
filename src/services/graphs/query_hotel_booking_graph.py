from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from src.services.graphs.agent_state import AgentState
from src.services.relative_db_service import relative_db_service
from src.utils.json import json_stringfy
from typing import List, Dict, Any, Optional


class HotelBookingInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0

def get_list_json_str(result: List[Dict[str, Any]]):
    """获取查询信息的展示数据"""
    dataList = [["id", "城市", "入住日期", "退房日期", "房型", "人数",], []]
    list = dataList[1]

    for info in result:
        data = [
            info["id"],
            info["city"],
            info["checkin_date"].strftime("%Y-%m-%d %H:%M"),
            info["checkout_date"].strftime("%Y-%m-%d %H:%M"),
            info["room_type"],
            info["guest_count"],
        ]
        list.append(data)

    return 'Type[List]' + json_stringfy(dataList)



def query_hotel_booking_graph() -> StateGraph:
    """查询酒店预订的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息提取和验证函数
    async def query(state: AgentState) -> AgentState:
        result = relative_db_service.list_hotel_bookings(state['user_id'])

        query = '已查询到您的酒店预定记录：'
        return {** state, "task_response": 2, "query": query + get_list_json_str(result)}

    # 添加节点到图中
    graph.add_node("query", query)
    # 设置图的入口点
    graph.set_entry_point("query")
    graph.add_edge("query", END)


    return graph