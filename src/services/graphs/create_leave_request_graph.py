from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_leave_request_graph() -> StateGraph:
    """创建请假申请工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state: AgentState):
        return {"message": "请提供请假类型、开始和结束日期及原因，我将为您提交申请。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph