from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from src.enums.LeaveRequest import LeaveRequestType
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getHistoryAndNextQuestion
from src.services.relative_db_service import relative_db_service
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional, List
from src.utils.getOpenAI import getChatOpenAI


class LeaveRequestInfo(BaseModel):
    """请假申请信息模型"""
    leave_type: Optional[str] = None            # 请假类型
    start_time: Optional[str] = None            # 开始时间 YYYY-MM-DD hh:ss
    end_time: Optional[str] = None              # 结束时间 YYYY-MM-DD hh:ss
    reason: Optional[str] = None                # 请假事由
    attachments: Optional[List[str]] = None     # 附加材料
    exit: Optional[int] = 0                     # 错误信息
    result: Optional[str] = None                # 申请结果


def create_leave_request_graph() -> StateGraph:
    """创建请假申请工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息收集节点
    async def collect_leave_type(state: AgentState):
        """收集请假类型"""
        response = await getHistoryAndNextQuestion("请选择请假类型：年假、病假、事假、婚假、产假、陪产假、丧假、调休假", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_response": 1}

    async def collect_start_time(state: AgentState):
        """收集开始时间"""
        response = await getHistoryAndNextQuestion("请提供开始时间（格式：YYYY-MM-DD hh:mm）", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_response": 1}

    async def collect_end_time(state: AgentState):
        """收集结束日期"""
        response = await getHistoryAndNextQuestion("请提供结束时间（格式：YYYY-MM-DD hh:mm）", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_response": 1}

    async def collect_reason(state: AgentState):
        """收集请假事由"""
        response = await getHistoryAndNextQuestion("请提供请假事由", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_response": 1}

    async def collect_attachments(state: AgentState):
        """收集附加材料"""
        prompt = "请提供相关证明材料"
        leave_type = state['task_collected']['leave_type']

        if leave_type == LeaveRequestType.SICK_LEAVE.text:
            prompt = "请提供医院诊断证明或病假单"
        elif leave_type == LeaveRequestType.MARRIAGE_LEAVE.text:
            prompt = "请提供结婚证复印件"
        elif leave_type == LeaveRequestType.MATERNITY_LEAVE.text or leave_type == LeaveRequestType.PATERNITY_LEAVE.text:
            prompt = "请提供出生证明复印件"

        response = await getHistoryAndNextQuestion(
            prompt,
            state['history'][-1],
            state['query']
        )

        return {** state, "query": response.content, "task_response": 1}

    async def goto_end(state: AgentState):
        response = await getHistoryAndNextQuestion("已退出", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_response": 2}

    # 定义信息提取和验证函数
    async def extract_info(state: AgentState) -> AgentState:
        booking_info = LeaveRequestInfo(**state.get("task_collected", {}))
        user_response = [*state["history"], state["query"]]

        # 创建LLM提示模板，用于解析和验证用户输入
        prompt = ChatPromptTemplate.from_template("""
        你是一个信息提取助手，需要从用户的回答中提取请假申请所需的信息。
        请根据用户当前的回答，提取相关信息并以JSON格式返回。
        当前已收集的信息: {existing_info}
        用户的回答: {user_response}
        需要提取的字段包括leave_type(请假类型), start_time(开始日期,格式YYYY-MM-DD hh:mm), end_time(结束日期,格式YYYY-MM-DD hh:mm), reason(请假事由), attachments(多个附件材料的名称)。
        如果用户的回答中包含多个字段信息，请全部提取。
        如果无法提取某个字段，保持该字段为null。
        请确保start_time和end_time字段符合YYYY-MM-DD hh:mm格式，如果不符合，请返回null。
        如果用户输入[退出/不想继续/取消/后悔/反悔]等意思，则增加字段exit为1，否则为0。
        只返回JSON，不要添加额外解释。
        """)

        # 初始化LLM和解析器
        llm = getChatOpenAI()
        parser = JsonOutputParser(pydantic_object=LeaveRequestInfo)

        # 调用LLM提取信息
        chain = prompt | llm | parser
        extracted_info = await chain.ainvoke({
            "existing_info": booking_info.dict(),
            "user_response": user_response
        })

        # 更新预订信息
        updated_info = booking_info.dict()
        for key, value in extracted_info.items():
            if value is not None:
                updated_info[key] = value

        return {** state, "task_collected": updated_info, "task_response": 0}

    def should_continue(state: AgentState) -> str:
        """判断是否需要继续收集信息"""
        booking_info = LeaveRequestInfo(**state.get("task_collected", {}))

        if booking_info.exit == 1:
            return "goto_end"
        if not booking_info.leave_type:
            return "collect_leave_type"
        elif not booking_info.start_time:
            return "collect_start_time"
        elif not booking_info.end_time:
            return "collect_end_time"
        elif not booking_info.reason:
            return "collect_reason"
        elif (booking_info.leave_type == LeaveRequestType.SICK_LEAVE.text
            or booking_info.leave_type == LeaveRequestType.MARRIAGE_LEAVE.text
            or booking_info.leave_type == LeaveRequestType.MATERNITY_LEAVE.text
            or booking_info.leave_type == LeaveRequestType.PATERNITY_LEAVE.text):
            if not booking_info.attachments:
                return "collect_attachments"

        return "save_to_database"



    # 定义数据库存储节点
    async def save_to_database(state: AgentState):
        booking_info = state["task_collected"]
        user_id = state["user_id"]

        # 调用数据库服务存储宾馆信息
        try:
            # 验证日期格式
            from datetime import datetime
            start_time = datetime.strptime(booking_info["start_time"], "%Y-%m-%d %H:%M")
            end_time = datetime.strptime(booking_info["end_time"], "%Y-%m-%d %H:%M")
            if start_time >= end_time:
                return {** state, "query": "开始时间必须晚于结束时间。", "error": "start_date less end_date", "task_response": 0}

            result = relative_db_service.create_leave_request(
                user_id=user_id,
                leave_type=booking_info["leave_type"],
                start_time=booking_info["start_time"],
                end_time=booking_info["end_time"],
                reason=booking_info["reason"],
                attachments=booking_info["attachments"]
            )

            return {** state, "query": f"请假申请成功！您的订单信息："
                                     f"[类型:{booking_info["leave_type"]} 开始时间:{booking_info["start_time"]} "
                                     f"结束时间:{booking_info["end_time"]} 原因:{booking_info["reason"]} "
                                     f"附件:{booking_info["attachments"]}]", "task_response": 2}
        except ValueError:
            return {** state, "query": "日期格式不正确，请使用YYYY-MM-DD hh:mm格式重试。", "error": "invalid_date_format", "task_response": 1}
        except Exception as e:
            return {** state, "query": f"请假申请失败：{str(e)}", "error": str(e), "task_response": 1}

    # 添加节点到图中
    graph.add_node("extract_info", extract_info)
    graph.add_node("collect_leave_type", collect_leave_type)
    graph.add_node("collect_start_time", collect_start_time)
    graph.add_node("collect_end_time", collect_end_time)
    graph.add_node("collect_reason", collect_reason)
    graph.add_node("collect_attachments", collect_attachments)
    graph.add_node("save_to_database", save_to_database)
    graph.add_node("goto_end", goto_end)
    # 设置图的入口点
    graph.set_entry_point("extract_info")

    # 添加节点之间的边
    graph.add_edge("collect_leave_type", END)
    graph.add_edge("collect_start_time", END)
    graph.add_edge("collect_end_time", END)
    graph.add_edge("collect_reason", END)
    graph.add_edge("collect_attachments", END)
    graph.add_edge("goto_end", END)

    # 设置条件边，根据信息收集情况决定下一步
    graph.add_conditional_edges(
        "extract_info",
        should_continue,
        {
            "collect_leave_type": "collect_leave_type",
            "collect_start_time": "collect_start_time",
            "collect_end_time": "collect_end_time",
            "collect_reason": "collect_reason",
            "collect_attachments": "collect_attachments",
            "save_to_database": "save_to_database",
            "goto_end": "goto_end"
        }
    )

    # 设置完成点
    graph.add_edge("save_to_database", END)

    return graph