from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_calendar_check_graph() -> StateGraph:
    """创建日历查询工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state):
        return {"message": "请提供您要查询的日期，我将为您检查日历安排。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph