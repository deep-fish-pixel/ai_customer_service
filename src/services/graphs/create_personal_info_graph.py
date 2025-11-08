from langgraph.graph import StateGraph
from src.services.graphs.agent_state import AgentState

def create_personal_info_graph() -> StateGraph:
    """创建个人信息查询工作流"""
    graph = StateGraph(AgentState)

    def collect_info(state: AgentState):
        return {"message": "请说明您要查询的个人信息类型(如昵称、联系方式、地址等),我将为您查找。"}

    graph.add_node("collect_info", collect_info)
    graph.set_entry_point("collect_info")
    graph.set_finish_point("collect_info")
    return graph