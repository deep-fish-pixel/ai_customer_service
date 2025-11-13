from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from src.enums.HotelBooking import HotelBookingTable
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getHistoryAndNextQuestion
from src.services.relative_db_service import relative_db_service
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import Optional
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


def create_hotel_booking_graph() -> StateGraph:
    """创建酒店预订工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息收集节点
    async def collect_city(state: AgentState):
        """收集城市信息"""
        response = await getHistoryAndNextQuestion("请问您计划入住的城市是哪里？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_checkin_date(state: AgentState):
        """收集入住日期"""
        response = await getHistoryAndNextQuestion("请问您的入住日期是什么时候？(格式：YYYY-MM-DD)", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_status": 1}

    async def collect_checkout_date(state: AgentState):
        """收集退房日期"""
        response = await getHistoryAndNextQuestion("请问您的退房日期是什么时候？(格式：YYYY-MM-DD)", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_room_type(state: AgentState):
        """收集房型信息"""
        response = await getHistoryAndNextQuestion("请问您需要什么类型的房间？(例如：标准间、大床房、套房)", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_status": 1}

    async def collect_guest_count(state: AgentState):
        """收集入住人数"""
        response = await getHistoryAndNextQuestion("请问入住人数是多少？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def goto_end(state: AgentState):
        response = await getHistoryAndNextQuestion("已退出", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 2}

    # 定义信息提取和验证函数
    async def extract_info(state: AgentState) -> AgentState:
        booking_info = HotelBookingInfo(**state.get("task_collected", {}))
        user_response = [*state["history"], state["query"]]

        # 创建LLM提示模板，用于解析和验证用户输入
        prompt = ChatPromptTemplate.from_template("""
        你是一个信息提取助手，需要从用户的回答中提取酒店预订所需的信息。
        请根据用户当前的回答，提取相关信息并以JSON格式返回。
        当前已收集的信息: {existing_info}
        用户的回答: {user_response}
        需要提取的字段包括city(入住城市), checkin_date(入住日期,格式YYYY-MM-DD), checkout_date(退房日期,格式YYYY-MM-DD), room_type(房间类型), guest_count(入住人数)。
        如果用户的回答中包含多个字段信息，请全部提取。
        如果无法提取某个字段，保持该字段为null。
        请确保checkin_date和checkout_date字段符合YYYY-MM-DD格式，如果不符合，请返回null。
        如果用户输入[退出/不想继续/取消/后悔/反悔]等意思，则增加字段exit为1，否则为0。
        只返回JSON，不要添加额外解释。
        """)

        # 初始化LLM和解析器
        llm = getChatOpenAI()
        parser = JsonOutputParser(pydantic_object=HotelBookingInfo)

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
        booking_info = HotelBookingInfo(**state.get("task_collected", {}))

        if booking_info.exit == 1:
            return "goto_end"
        if not booking_info.city:
            return "collect_city"
        elif not booking_info.checkin_date:
            return "collect_checkin_date"
        elif not booking_info.checkout_date:
            return "collect_checkout_date"
        elif not booking_info.room_type:
            return "collect_room_type"
        elif not booking_info.guest_count:
            return "collect_guest_count"
        else:
            return "save_to_database"


    # 定义数据库存储节点
    async def save_to_database(state: AgentState):
        booking_info = state["task_collected"]
        user_id = state["user_id"]

        # 调用数据库服务存储酒店信息
        try:
            # 验证日期格式
            from datetime import datetime
            checkin = datetime.strptime(booking_info["checkin_date"], "%Y-%m-%d").replace(hour=12, minute=0, second=0)
            checkout = datetime.strptime(booking_info["checkout_date"], "%Y-%m-%d").replace(hour=12, minute=0, second=0)
            if checkout <= checkin:
                return {** state, "query": "退房日期必须晚于入住日期。", "error": "start_date_less_end_date", "task_status": 0}

            result = relative_db_service.create_hotel_booking(
                user_id=user_id,
                city=booking_info["city"],
                checkin_date=checkin,
                checkout_date=checkout,
                room_type=booking_info["room_type"],
                guest_count=booking_info["guest_count"]
            )
            return {** state, "booking_result": result, "query": f"酒店预订成功！您的订单信息：{HotelBookingTable.get_list_json_str([result])}", "task_status": 2}
        except ValueError:
            return {** state, "query": "日期格式不正确，请使用YYYY-MM-DD格式重试。", "error": "invalid_date_format", "task_status": 1}
        except Exception as e:
            return {** state, "query": f"预订失败：{str(e)}", "error": str(e), "task_status": 1}

    # 添加节点到图中
    graph.add_node("extract_info", extract_info)
    graph.add_node("collect_city", collect_city)
    graph.add_node("collect_checkin_date", collect_checkin_date)
    graph.add_node("collect_checkout_date", collect_checkout_date)
    graph.add_node("collect_room_type", collect_room_type)
    graph.add_node("collect_guest_count", collect_guest_count)
    graph.add_node("save_to_database", save_to_database)
    graph.add_node("goto_end", goto_end)
    # 设置图的入口点
    graph.set_entry_point("extract_info")

    # 添加节点之间的边
    graph.add_edge("collect_city", END)
    graph.add_edge("collect_checkin_date", END)
    graph.add_edge("collect_checkout_date", END)
    graph.add_edge("collect_room_type", END)
    graph.add_edge("collect_guest_count", END)
    graph.add_edge("goto_end", END)

    # 设置条件边，根据信息收集情况决定下一步
    graph.add_conditional_edges(
        "extract_info",
        should_continue,
        {
            "collect_city": "collect_city",
            "collect_checkin_date": "collect_checkin_date",
            "collect_checkout_date": "collect_checkout_date",
            "collect_room_type": "collect_room_type",
            "collect_guest_count": "collect_guest_count",
            "save_to_database": "save_to_database",
            "goto_end": "goto_end"
        }
    )

    # 设置完成点
    graph.add_edge("save_to_database", END)

    return graph