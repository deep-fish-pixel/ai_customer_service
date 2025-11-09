from langgraph.graph import StateGraph, END

from src.enums.ScheduleMeeting import ScheduleMeetingType, MeetingType
from src.services.graphs.agent_state import AgentState
from src.services.relative_db_service import relative_db_service


def query_leave_request_graph() -> StateGraph:
    """查询请假申请的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息提取和验证函数
    async def query(state: AgentState) -> AgentState:
        result = relative_db_service.list_hotel_bookings(state['user_id'])

        query = '已查询到您的请假申请如下：'

        for info in result:
            query += (f"[标题:{info["title"]} 日程类型:{ScheduleMeetingType.get_text_by_value(info["type"])} "
                      f"会议类型:{MeetingType.get_text_by_value(info["meeting_type"])} 会议室:{info["meeting_room"]} 日期:{info["start_time"]} "
                      f"会议时长:{(info["start_time"] - info["end_time"]) / 60 }分钟 参与者:{info["participants"]}]")

        return {** state, "task_response": 2, "query": query}

    # 添加节点到图中
    graph.add_node("query", query)
    # 设置图的入口点
    graph.set_entry_point("query")
    graph.add_edge("query", END)


    return graph