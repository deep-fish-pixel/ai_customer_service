from langgraph.graph import StateGraph, END

from src.enums.ScheduleMeeting import ScheduleMeetingType, MeetingType
from src.services.graphs.agent_state import AgentState
from src.services.relative_db_service import relative_db_service


def query_leave_request_graph() -> StateGraph:
    """查询请假申请的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息提取和验证函数
    async def query(state: AgentState) -> AgentState:
        result = relative_db_service.list_leave_requests(state['user_id'])

        query = '已查询到您的请假申请如下：'

        for info in result:
            query += (f"[类型:{info["leave_type"]} 开始时间:{info["start_time"]} "
                      f"结束时间:{info["end_time"]} 原因:{info["reason"]} "
                      f"{"附件:" + info["attachments"] if info["attachments"] else ''}]")

        return {** state, "task_response": 2, "query": query}

    # 添加节点到图中
    graph.add_node("query", query)
    # 设置图的入口点
    graph.set_entry_point("query")
    graph.add_edge("query", END)


    return graph