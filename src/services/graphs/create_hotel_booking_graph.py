from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_hotel_booking_graph() -> StateGraph:
    """创建酒店预订工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state: AgentState):
        return {"message": "请提供您的入住城市、入住和退房日期，我将为您预订酒店。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph