from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_meeting_scheduling_graph() -> StateGraph:
    """创建会议安排工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state: AgentState):
        return {"message": "请提供会议主题、参与者、日期和时间，我将为您安排会议。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph