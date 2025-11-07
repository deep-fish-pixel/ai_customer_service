from langgraph.graph import StateGraph, END
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getHistoryAndNextQuestion
from src.services.relative_db_service import relative_db_service
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import datetime

from src.utils.getOpenAI import getChatOpenAI


class HotelBookingInfo(BaseModel):
    """酒店预订信息模型"""
    city: Optional[str] = None
    checkin_date: Optional[str] = None
    checkout_date: Optional[str] = None
    room_type: Optional[str] = None
    guest_count: Optional[int] = None
    booking_result: Optional[str] = None
    exit: Optional[int] = 0
    error: Optional[str] = None

# 更新AgentState以包含酒店预订信息
class AgentState:
    history: list
    query: str
    user_id: int
    hotel_booking: HotelBookingInfo = HotelBookingInfo()
    task_response: int = 0
    exit: int = 0

async def extract_info(state: AgentState) -> AgentState:
    """使用LLM提取和验证酒店预订信息"""
    if not state.query:
        return state

    # 定义输出格式
    class InfoParser(HotelBookingInfo):
        class Config:
            extra = "allow"

    parser = JsonOutputParser(pydantic_object=InfoParser)

    # 创建提示模板
    # prompt = ChatPromptTemplate.from_template("""
    #     你是一个信息提取助手，需要从用户的回答中提取航班预订所需的信息。
    #     请根据用户当前的回答，提取相关信息并以JSON格式返回。
    #     当前已收集的信息: {existing_info}
    #     用户的回答: {user_response}
    #     需要提取的字段包括origin(城市), destination(终点), date(时间,格式YYYY-MM-DD), seat_class(座位等级), seat_preference(座位偏好)。
    #     如果用户的回答中包含多个字段信息，请全部提取。
    #     如果无法提取某个字段，保持该字段为null。
    #     请确保date字段符合YYYY-MM-DD格式，如果不符合，请返回null。
    #     如果用户输入[退出/不想继续/取消/后悔/反悔]等意思，则增加字段exit为1，否则为0。
    #     只返回JSON，不要添加额外解释。
    #     """)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "您是酒店预订信息提取专家。请从用户输入中提取并验证酒店预订所需信息。"),
        ("system", f"当前已收集信息: {state.hotel_booking.dict()}"),
        ("system", "需要收集的信息: {['城市', '入住日期(YYYY-MM-DD)', '退房日期(YYYY-MM-DD)', '房型', '人数']}"),
        ("user", "用户输入: {input}"),
        ("system", f"请以JSON格式输出，确保日期格式正确且退房日期晚于入住日期。{parser.get_format_instructions()}")
    ])

    # 调用LLM
    model = getChatOpenAI()
    chain = prompt | model | parser

    try:
        result = await chain.ainvoke({
            "input": state.query,
            "booking_info": state.hotel_booking.dict()
        })

        # 更新状态中的预订信息
        for key, value in result.items():
            if value and hasattr(state.hotel_booking, key):
                setattr(state.hotel_booking, key, value)

        # 验证日期
        if state.hotel_booking.checkin_date and state.hotel_booking.checkout_date:
            try:
                checkin = datetime.datetime.strptime(state.hotel_booking.checkin_date, "%Y-%m-%d")
                checkout = datetime.datetime.strptime(state.hotel_booking.checkout_date, "%Y-%m-%d")
                if checkout <= checkin:
                    state.hotel_booking.error = "退房日期必须晚于入住日期"
            except ValueError:
                state.hotel_booking.error = "日期格式不正确，请使用YYYY-MM-DD格式"

    except Exception as e:
        state.hotel_booking.error = f"信息提取失败: {str(e)}"

    return state

async def should_continue(state: AgentState) -> str:
    """判断是否需要继续收集信息"""
    if state.hotel_booking.error:
        return "collect_info"

    # 检查是否所有信息都已收集
    required_fields = ["city", "checkin_date", "checkout_date", "room_type", "guest_count"]
    missing_fields = [field for field in required_fields if not getattr(state.hotel_booking, field)]

    if not missing_fields:
        return "save_to_database"
    
    # 根据缺失字段决定下一个收集节点
    next_field = missing_fields[0]
    return f"collect_{next_field}"

async def collect_city(state: AgentState):
    """收集城市信息"""
    response = await getHistoryAndNextQuestion(
        "请问您计划入住的城市是哪里？",
        state.history[-1] if state.history else "",
        state.query
    )
    return {**state, "query": response.content, "task_response": 1}

async def collect_checkin_date(state: AgentState):
    """收集入住日期"""
    response = await getHistoryAndNextQuestion(
        "请问您的入住日期是什么时候？(格式：YYYY-MM-DD)",
        state.history[-1] if state.history else "",
        state.query
    )
    return {**state, "query": response.content, "task_response": 1}

async def collect_checkout_date(state: AgentState):
    """收集退房日期"""
    response = await getHistoryAndNextQuestion(
        "请问您的退房日期是什么时候？(格式：YYYY-MM-DD)",
        state.history[-1] if state.history else "",
        state.query
    )
    return {**state, "query": response.content, "task_response": 1}

async def collect_room_type(state: AgentState):
    """收集房型信息"""
    response = await getHistoryAndNextQuestion(
        "请问您需要什么类型的房间？(例如：标准间、大床房、套房)",
        state.history[-1] if state.history else "",
        state.query
    )
    return {**state, "query": response.content, "task_response": 1}

async def collect_guest_count(state: AgentState):
    """收集入住人数"""
    response = await getHistoryAndNextQuestion(
        "请问入住人数是多少？",
        state.history[-1] if state.history else "",
        state.query
    )
    return {**state, "query": response.content, "task_response": 1}

async def save_to_database(state: AgentState) -> AgentState:
    """保存酒店预订信息到数据库"""
    try:
        # 调用酒店预订接口
        result = relative_db_service.create_hotel_booking(
            user_id=state.user_id,
            city=state.hotel_booking.city,
            checkin_date=state.hotel_booking.checkin_date,
            checkout_date=state.hotel_booking.checkout_date,
            room_type=state.hotel_booking.room_type,
            guest_count=state.hotel_booking.guest_count
        )

        if result:
            state.hotel_booking.booking_result = result
            state.task_response = 2
            state.query  = (
                f"酒店预订成功！您的订单信息：\n"
                f"城市：{state.hotel_booking.city}\n"
                f"入住日期：{state.hotel_booking.checkin_date}\n"
                f"退房日期：{state.hotel_booking.checkout_date}\n"
                f"房型：{state.hotel_booking.room_type}\n"
                f"人数：{state.hotel_booking.guest_count}"
            )
        else:
            state.hotel_booking.error = "酒店预订失败，请稍后重试"

    except Exception as e:
        state.hotel_booking.error = f"预订处理失败: {str(e)}"

    return state

def create_hotel_booking_graph() -> StateGraph:
    """创建酒店预订工作流"""
    graph = StateGraph(AgentState)

    # 添加节点
    graph.add_node("extract_info", extract_info)
    graph.add_node("should_continue", should_continue)
    graph.add_node("collect_city", collect_city)
    graph.add_node("collect_checkin_date", collect_checkin_date)
    graph.add_node("collect_checkout_date", collect_checkout_date)
    graph.add_node("collect_room_type", collect_room_type)
    graph.add_node("collect_guest_count", collect_guest_count)
    graph.add_node("save_to_database", save_to_database)

    # 设置入口点
    graph.set_entry_point("extract_info")

    # 添加边
    graph.add_edge("extract_info", "should_continue")
    graph.add_edge("save_to_database", END)

    # 设置条件边
    graph.add_conditional_edges(
        "should_continue",
        lambda x: x,
        {
            "collect_city": "collect_city",
            "collect_checkin_date": "collect_checkin_date",
            "collect_checkout_date": "collect_checkout_date",
            "collect_room_type": "collect_room_type",
            "collect_guest_count": "collect_guest_count",
            "save_to_database": "save_to_database",
            "collect_info": "collect_city"
        }
    )

    # 从收集节点回到信息提取节点
    for node in ["collect_city", "collect_checkin_date", "collect_checkout_date", "collect_room_type", "collect_guest_count"]:
        graph.add_edge(node, "extract_info")

    return graph