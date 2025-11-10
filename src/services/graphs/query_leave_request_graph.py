from langgraph.graph import StateGraph, END

from src.enums.ScheduleMeeting import ScheduleMeetingType, MeetingType
from src.services.graphs.agent_state import AgentState
from src.services.relative_db_service import relative_db_service
from src.utils.json import json_stringfy
from typing import List, Dict, Any, Optional

def get_list_json_str(result: List[Dict[str, Any]]):
    """获取查询信息的展示数据"""
    dataList = [["id", "类型", "开始时间", "结束时间", "原因", "附件",], []]
    list = dataList[1]

    for info in result:
        data = [
            info["id"],
            info["leave_type"],
            info["start_time"].strftime("%Y-%m-%d %H:%M"),
            info["end_time"].strftime("%Y-%m-%d %H:%M"),
            info["reason"],
            info["attachments"],
        ]
        list.append(data)

    return 'Type[List]' + json_stringfy(dataList)




def query_leave_request_graph() -> StateGraph:
    """查询请假申请的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息提取和验证函数
    async def query(state: AgentState) -> AgentState:
        result = relative_db_service.list_leave_requests(state['user_id'])
        query = '已查询到您的请假申请记录：'
        return {** state, "task_response": 2, "query": query + get_list_json_str(result)}

    # 添加节点到图中
    graph.add_node("query", query)
    # 设置图的入口点
    graph.set_entry_point("query")
    graph.add_edge("query", END)


    return graph