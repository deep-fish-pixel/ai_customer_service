from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_calendar_check_graph() -> StateGraph:
    """创建日历查询工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state):
        #提前5分钟、15分钟、1小时或1天提醒
        return {"message": "请提供日程的标题、类型（会议、专注时间、私人事务）、参与者、会议类型（线上下会议：会议室名称，线上会议：会议链接）、日期、起止时间、 我将为您安排会议。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph