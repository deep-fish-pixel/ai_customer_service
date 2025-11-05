from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_weather_check_graph() -> StateGraph:
    """创建天气查询工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state: AgentState):
        return {"message": "请提供您要查询的城市和日期，我将为您获取天气信息。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph