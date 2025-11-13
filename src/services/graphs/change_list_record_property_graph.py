from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from src.enums import get_table_info, get_table_name, get_column_name
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getHistoryAndNextQuestion
from src.services.relative_db_service import relative_db_service
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional
from src.utils.getOpenAI import getChatOpenAI
from src.enums.JsonSeperator import JsonSeperator


class UpdateInfo(BaseModel):
    id: Optional[int] = None
    record_type: Optional[str] = None
    index: Optional[int] = None
    property_name: Optional[str] = None
    new_value: Optional[str|int] = None
    size: Optional[int] = None
    exit: Optional[int] = 0


def change_list_record_property_graph() -> StateGraph:
    """创建修改列表记录的属性值工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息收集节点
    async def collect_record_type(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您要修改的类型是？（日程会议/请假申请/预定机票/预定酒店）", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_index(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您要修改的是第几条？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_property_name(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您要修改的属性名称是？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_new_value(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您要修改的新值是？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_id(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您要修改的id是？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def goto_end(state: AgentState):
        response = await getHistoryAndNextQuestion("已退出", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 2}


    # 定义信息提取和验证函数
    async def extract_info(state: AgentState) -> AgentState:
        task_collected = state.get("task_collected", {})
        if 'id' in task_collected and isinstance(task_collected['id'], int):
            task_collected['id'] = str(task_collected['id'])
        update_info = UpdateInfo(**task_collected)
        user_response = [*state["history"], state["query"]]

        # 创建LLM提示模板，用于解析和验证用户输入
        prompt = ChatPromptTemplate.from_template("""
        你是一个信息提取助手，需要从用户的回答中提取修改列表第n个记录的某个字段名称所需的信息。
        请根据用户当前的回答，提取相关信息并以JSON格式返回。
        当前已收集的信息: {existing_info}
        用户的回答: {user_response}
        需要提取的字段包括id(id，需要根据列表的index获取到)，record_type(记录类型(日程会议/请假申请/预定机票/预定酒店)，不需要包含(记录/信息)2个字)，index(序号，默认从1开始，如果记录只有一条，默认1，对应数据的下标为index-1)，property_name(属性名称)，new_value(新值)，size(列表的总数)。
        如果用户的回答中包含多个字段信息，请全部提取。
        如果无法提取某个字段，保持该字段为null。
        如果用户输入[退出/不想继续/取消/后悔/反悔]等意思，则增加字段exit为1，否则为0。
        只返回JSON，不要添加额外解释。
        """)

        # 初始化LLM和解析器
        llm = getChatOpenAI()
        parser = JsonOutputParser(pydantic_object=UpdateInfo)

        # 调用LLM提取信息
        chain = prompt | llm | parser
        extracted_info = await chain.ainvoke({
            "existing_info": update_info.dict(),
            "user_response": user_response
        })

        # 更新预订信息
        updated_info = update_info.dict()
        for key, value in extracted_info.items():
            if value is not None:
                updated_info[key] = value

        return {** state, "task_collected": updated_info, "task_status": 0}

    # 定义决策节点，判断是否需要继续收集信息
    def should_continue(state: AgentState) -> str:
        update_info = UpdateInfo(**state.get("task_collected", {}))

        if update_info.exit == 1:
            return "goto_end"
        if not update_info.record_type:
            return "collect_record_type"
        if not update_info.index:
            return "collect_index"
        if not update_info.property_name:
            return "collect_property_name"
        if not update_info.new_value:
            return "collect_new_value"
        if not update_info.id:
            return "collect_id"
        else:
            return "save_to_database"

    # 定义数据库存储节点
    async def save_to_database(state: AgentState):
        update_info = state["task_collected"]

        # 调用数据库服务存储机票信息
        try:
            table_info = get_table_info(update_info["record_type"])
            table_name = get_table_name(update_info["record_type"])
            column_name = get_column_name(table_info, update_info["property_name"])

            record = relative_db_service.query_table_record(
                table_name=table_name,
                id=update_info["id"],
            )

            valid_message = table_info.valide_value(column=column_name, new_value=update_info["new_value"], record=record)

            if (valid_message):
                return {** state, "query": f"预订失败：{valid_message}", "task_status": 1}

            result = relative_db_service.update_table_column(
                table_name=table_name,
                id=update_info["id"],
                column_name=column_name,
                new_value=table_info.handle_value(column_name, update_info["new_value"], record),
            )
            if (result):
                records = []
                if (update_info["size"] == 1):
                    records = [relative_db_service.query_table_record(
                        table_name=table_name,
                        id=update_info["id"],
                    )]
                else:
                    records = relative_db_service.query_table_records(
                        user_id=state["user_id"],
                        table_name=table_name,
                    )
                return {** state, "query": f"{update_info["record_type"]}的{update_info["property_name"]}修改成功！{table_info.get_list_json_str(records)}", "task_status": 2}
            return {** state, "query": f"{update_info["property_name"]}修改失败！", "task_status": 2}
        except Exception as e:
            return {** state, "query": f"预订失败：{str(e)}", "error": str(e), "task_status": 1}

    # 添加节点到图中
    graph.add_node("extract_info", extract_info)
    graph.add_node("collect_record_type", collect_record_type)
    graph.add_node("collect_index", collect_index)
    graph.add_node("collect_property_name", collect_property_name)
    graph.add_node("collect_new_value", collect_new_value)
    graph.add_node("collect_id", collect_id)
    graph.add_node("save_to_database", save_to_database)
    graph.add_node("goto_end", goto_end)
    # 设置图的入口点
    graph.set_entry_point("extract_info")

    # 添加节点之间的边
    graph.add_edge("collect_record_type", END)
    graph.add_edge("collect_index", END)
    graph.add_edge("collect_property_name", END)
    graph.add_edge("collect_new_value", END)
    graph.add_edge("collect_id", END)
    graph.add_edge("goto_end", END)

    # 设置条件边，根据信息收集情况决定下一步
    graph.add_conditional_edges(
        "extract_info",
        should_continue,
        {
            "collect_record_type": "collect_record_type",
            "collect_index": "collect_index",
            "collect_property_name": "collect_property_name",
            "collect_new_value": "collect_new_value",
            "collect_id": "collect_id",
            "save_to_database": "save_to_database",
            "goto_end": "goto_end"
        }
    )

    # 设置完成点
    graph.add_edge("save_to_database", END)

    return graph