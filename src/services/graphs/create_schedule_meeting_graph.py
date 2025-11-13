from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from src.enums.ScheduleMeeting import ScheduleMeetingType, MeetingType, ScheduleMeetingTable
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getHistoryAndNextQuestion
from src.services.relative_db_service import relative_db_service
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional, List
from src.utils.getOpenAI import getChatOpenAI


class ScheduleMeetingInfo(BaseModel):
    """日程会议信息模型"""
    title: Optional[str] = None
    type: Optional[str] = None  # 会议、专注时间、私人事务
    meeting_type: Optional[str] = None  # 线上会议或线下会议
    meeting_room: Optional[str] = None  # 线上会议链接或线下会议室名称
    start_time: Optional[str] = None  # 格式: YYYY-MM-DD hh:mm
    duration: Optional[int] = None  # 格式: 60m
    participants: Optional[List[str]] = None
    exit: Optional[int] = 0
    result: Optional[str] = None


def create_schedule_meeting_graph() -> StateGraph:
    """创建日程会议工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息收集节点
    async def collect_title(state: AgentState):
        """收集会议标题"""
        response = await getHistoryAndNextQuestion("请提供会议标题？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_type(state: AgentState):
        """收集会议类型"""
        response = await getHistoryAndNextQuestion("请选择日程类型：会议、专注时间、私人事务", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_status": 1}

    async def collect_meeting_type(state: AgentState):
        """收集会议形式信息"""
        response = await getHistoryAndNextQuestion("请提供会议类型（线上会议、线下会议）", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_status": 1}

    async def collect_meeting_room(state: AgentState):
        """收集线下意义的会议室名称"""
        response = await getHistoryAndNextQuestion("请提供会议室名称", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_status": 1}

    async def collect_start_time(state: AgentState):
        """收集会议开始时间"""
        response = await getHistoryAndNextQuestion(f"请提供开始时间（格式：YYYY-MM-DD hh-mm）", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_duration(state: AgentState):
        """收集会议起止时间"""
        response = await getHistoryAndNextQuestion("请提供时长（单位分钟）", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_participants(state: AgentState):
        """收集参与者信息"""
        response = await getHistoryAndNextQuestion("请提供会议参与者（多个参与者用逗号分隔）", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def goto_end(state: AgentState):
        response = await getHistoryAndNextQuestion("已退出", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 2}

    # 定义信息提取和验证函数
    async def extract_info(state: AgentState) -> AgentState:
        booking_info = ScheduleMeetingInfo(**state.get("task_collected", {}))
        user_response = [*state["history"], state["query"]]

        # 创建LLM提示模板，用于解析和验证用户输入
        prompt = ChatPromptTemplate.from_template("""
        你是一个信息提取助手，需要从用户的回答中提取日程会议所需的信息。
        请根据用户当前的回答，提取相关信息并以JSON格式返回。
        当前已收集的信息: {existing_info}
        用户的回答: {user_response}
        需要提取的字段包括title(标题), type(日程类型), meeting_type(会议类型), meeting_room(会议室), start_time(日期,格式YYYY-MM-DD hh:mm), duration(会议时长,要求：数字类型单位分钟), room_type(房间类型), participants(参与者)。
        如果用户的回答中包含多个字段信息，请全部提取。
        如果无法提取某个字段，保持该字段为null。
        请确保start_time字段符合YYYY-MM-DD格式，如果不符合，请返回null。
        如果用户输入[退出/不想继续/取消/后悔/反悔]等意思，则增加字段exit为1，否则为0。
        只返回JSON，不要添加额外解释。
        """)

        # 初始化LLM和解析器
        llm = getChatOpenAI()
        parser = JsonOutputParser(pydantic_object=ScheduleMeetingInfo)

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

        return {** state, "task_collected": updated_info, "task_status": 0}

    def should_continue(state: AgentState) -> str:
        """判断是否需要继续收集信息"""
        booking_info = ScheduleMeetingInfo(**state.get("task_collected", {}))

        if booking_info.exit == 1:
            return "goto_end"
        if not booking_info.title:
            return "collect_title"
        elif not booking_info.type:
            return "collect_type"
        elif not booking_info.start_time:
            return "collect_start_time"
        elif not booking_info.duration:
            return "collect_duration"
        elif booking_info.type == ScheduleMeetingType.MEETING.text:
            if not booking_info.meeting_type:
                return "collect_meeting_type"
            elif not booking_info.meeting_room:
                return "collect_meeting_room"
            elif not booking_info.participants:
                return "collect_participants"

        return "save_to_database"


    # 定义数据库存储节点
    async def save_to_database(state: AgentState):
        booking_info = state["task_collected"]
        user_id = state["user_id"]

        # 调用数据库服务存储酒店信息
        try:
            # 验证日期格式
            from datetime import datetime, timedelta
            start_time = datetime.strptime(booking_info["start_time"], "%Y-%m-%d %H:%M")
            end_time = start_time +  timedelta(minutes=booking_info["duration"])

            result = relative_db_service.create_schedule_meeting(
                user_id=user_id,
                title=booking_info["title"],
                type=ScheduleMeetingType.get_value_by_text(booking_info["type"]),
                meeting_type=MeetingType.get_value_by_text(booking_info["meeting_type"]),
                meeting_room=booking_info["meeting_room"],
                start_time=start_time,
                end_time=end_time,
                participants=booking_info["participants"]
            )
            return {
                ** state,
                "result": result,
                "query": f"日程会议成功！日程会议信息：{ScheduleMeetingTable.get_list_json_str([result])}",
                    "task_status": 2
            }
        except ValueError:
            return {** state, "query": "日期格式不正确，请使用YYYY-MM-DD hh:mm格式重试。", "error": "invalid_date_format", "task_status": 1}
        except Exception as e:
            return {** state, "query": f"创建日程会议失败：{str(e)}", "error": str(e), "task_status": 1}

    # 添加节点到图中
    graph.add_node("extract_info", extract_info)
    graph.add_node("collect_title", collect_title)
    graph.add_node("collect_type", collect_type)
    graph.add_node("collect_meeting_type", collect_meeting_type)
    graph.add_node("collect_meeting_room", collect_meeting_room)
    graph.add_node("collect_start_time", collect_start_time)
    graph.add_node("collect_duration", collect_duration)
    graph.add_node("collect_participants", collect_participants)
    graph.add_node("save_to_database", save_to_database)
    graph.add_node("goto_end", goto_end)
    # 设置图的入口点
    graph.set_entry_point("extract_info")

    # 添加节点之间的边
    graph.add_edge("collect_title", END)
    graph.add_edge("collect_type", END)
    graph.add_edge("collect_meeting_type", END)
    graph.add_edge("collect_meeting_room", END)
    graph.add_edge("collect_start_time", END)
    graph.add_edge("collect_duration", END)
    graph.add_edge("collect_participants", END)
    graph.add_edge("goto_end", END)

    # 设置条件边，根据信息收集情况决定下一步
    graph.add_conditional_edges(
        "extract_info",
        should_continue,
        {
            "collect_title": "collect_title",
            "collect_type": "collect_type",
            "collect_meeting_type": "collect_meeting_type",
            "collect_meeting_room": "collect_meeting_room",
            "collect_start_time": "collect_start_time",
            "collect_duration": "collect_duration",
            "collect_participants": "collect_participants",
            "save_to_database": "save_to_database",
            "goto_end": "goto_end"
        }
    )

    # 设置完成点
    graph.add_edge("save_to_database", END)

    return graph