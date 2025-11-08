from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_leave_request_graph() -> StateGraph:
    """创建请假申请工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state: AgentState):
        return {"message": "请提供请假类型(年假、病假、事假、婚假、产假、陪产假、丧假、调休假)、开始日期和结束日期、请假事由、附加材料（病假：医院诊断证明、病假单。婚假/产假：结婚证、出生证明等复印件），我将为您提交申请。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph