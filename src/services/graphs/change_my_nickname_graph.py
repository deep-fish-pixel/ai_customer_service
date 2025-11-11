from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from src.services.graphs.agent_state import AgentState
from src.services.graphs.query_flight_booking_graph import get_list_json_str
from src.services.graphs.utils import getHistoryAndNextQuestion
from src.services.relative_db_service import relative_db_service
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional
from src.utils.getOpenAI import getChatOpenAI
from src.enums.JsonSeperator import JsonSeperator


class AccountInfo(BaseModel):
    id: Optional[str] = None
    new_nickname: Optional[str] = None
    exit: Optional[int] = 0


def change_my_nickname_graph() -> StateGraph:
    """创建航班预订工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息收集节点
    async def collect_nickname(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您的新昵称是？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def goto_end(state: AgentState):
        response = await getHistoryAndNextQuestion("已退出", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 2}


    # 定义信息提取和验证函数
    async def extract_info(state: AgentState) -> AgentState:
        account_info = AccountInfo(**state.get("task_collected", {}))
        user_response = [*state["history"], state["query"]]

        # 创建LLM提示模板，用于解析和验证用户输入
        prompt = ChatPromptTemplate.from_template("""
        你是一个信息提取助手，需要从用户的回答中提取航班预订所需的信息。
        请根据用户当前的回答，提取相关信息并以JSON格式返回。
        当前已收集的信息: {existing_info}
        用户的回答: {user_response}
        需要提取的字段包括new_nickname(新昵称)。
        如果用户的回答中包含多个字段信息，请全部提取。
        如果无法提取某个字段，保持该字段为null。
        如果用户输入[退出/不想继续/取消/后悔/反悔]等意思，则增加字段exit为1，否则为0。
        只返回JSON，不要添加额外解释。
        """)

        # 初始化LLM和解析器
        llm = getChatOpenAI()
        parser = JsonOutputParser(pydantic_object=AccountInfo)

        # 调用LLM提取信息
        chain = prompt | llm | parser
        extracted_info = await chain.ainvoke({
            "existing_info": account_info.dict(),
            "user_response": user_response
        })

        # 更新预订信息
        updated_info = account_info.dict()
        for key, value in extracted_info.items():
            if value is not None:
                updated_info[key] = value

        return {** state, "task_collected": updated_info, "task_status": 0}

    # 定义决策节点，判断是否需要继续收集信息
    def should_continue(state: AgentState) -> str:
        account_info = AccountInfo(**state.get("task_collected", {}))

        if account_info.exit == 1:
            return "goto_end"
        if not account_info.new_nickname:
            return "collect_nickname"
        else:
            return "save_to_database"


    # 定义数据库存储节点
    async def save_to_database(state: AgentState):
        account_info = state["task_collected"]
        user_id = state["user_id"]

        # 调用数据库服务存储机票信息
        try:
            result = relative_db_service.change_nickname(
                user_id=user_id,
                new_nickname=account_info["new_nickname"],
            )
            return {** state, "query": f"昵称修改成功！您的新昵称是：{result["nickname"]}{JsonSeperator.CALL_GET_USER_INFO}", "task_status": 2}
        except Exception as e:
            return {** state, "query": f"预订失败：{str(e)}", "error": str(e), "task_status": 0}

    # 添加节点到图中
    graph.add_node("extract_info", extract_info)
    graph.add_node("collect_nickname", collect_nickname)
    graph.add_node("save_to_database", save_to_database)
    graph.add_node("goto_end", goto_end)
    # 设置图的入口点
    graph.set_entry_point("extract_info")

    # 添加节点之间的边
    graph.add_edge("collect_nickname", END)
    graph.add_edge("goto_end", END)

    # 设置条件边，根据信息收集情况决定下一步
    graph.add_conditional_edges(
        "extract_info",
        should_continue,
        {
            "collect_nickname": "collect_nickname",
            "save_to_database": "save_to_database",
            "goto_end": "goto_end"
        }
    )

    # 设置完成点
    graph.add_edge("save_to_database", END)

    return graph