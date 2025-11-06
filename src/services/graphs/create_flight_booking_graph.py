from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_flight_booking_graph() -> StateGraph:
    """创建航班预订工作流"""

    graph = StateGraph(AgentState)

    def collect_info(state: AgentState):
        return {
            **state,
            "query": "请提供您的出发城市、目的地和出行日期，我将为您预订航班。",
        }

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph