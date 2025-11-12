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


class FlightBookingInfo(BaseModel):
    id: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    start_time: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0


def create_flight_booking_graph() -> StateGraph:
    """创建航班预订工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息收集节点
    async def collect_origin(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您的出发城市是哪里？", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_destination(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您的目的地城市是哪里？", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_status": 1}

    async def collect_start_time(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您的出行日期是什么时候？(格式：YYYY-MM-DD hh:mm)", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def collect_seat_class(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您需要什么座位等级？(经济舱/商务舱/头等舱)", state['history'][-1], state['query'])

        return {**state, "query": response.content, "task_status": 1}

    async def collect_seat_preference(state: AgentState):
        response = await getHistoryAndNextQuestion("请问您有什么座位偏好？(靠窗/靠过道/中间/无偏好)", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 1}

    async def goto_end(state: AgentState):
        response = await getHistoryAndNextQuestion("已退出", state['history'][-1], state['query'])

        return {** state, "query": response.content, "task_status": 2}

    # 定义信息提取和验证函数
    async def extract_info(state: AgentState) -> AgentState:
        booking_info = FlightBookingInfo(**state.get("task_collected", {}))
        user_response = [*state["history"], state["query"]]

        # 创建LLM提示模板，用于解析和验证用户输入
        prompt = ChatPromptTemplate.from_template("""
        你是一个信息提取助手，需要从用户的回答中提取航班预订所需的信息。
        请根据用户当前的回答，提取相关信息并以JSON格式返回。
        当前已收集的信息: {existing_info}
        用户的回答: {user_response}
        需要提取的字段包括origin(起点), destination(终点), start_time(时间,格式YYYY-MM-DD hh:mm), seat_class(座位等级), seat_preference(座位偏好)。
        如果用户的回答中包含多个字段信息，请全部提取。
        如果无法提取某个字段，保持该字段为null。
        请确保date字段符合YYYY-MM-DD格式，如果不符合，请返回null。
        如果用户输入[退出/不想继续/取消/后悔/反悔]等意思，则增加字段exit为1，否则为0。
        只返回JSON，不要添加额外解释。
        """)

        # 初始化LLM和解析器
        llm = getChatOpenAI()
        parser = JsonOutputParser(pydantic_object=FlightBookingInfo)

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

    # 定义决策节点，判断是否需要继续收集信息
    def should_continue(state: AgentState) -> str:
        booking_info = FlightBookingInfo(**state.get("task_collected", {}))

        if booking_info.exit == 1:
            return "goto_end"
        if not booking_info.origin:
            return "collect_origin"
        elif not booking_info.destination:
            return "collect_destination"
        elif not booking_info.start_time:
            return "collect_start_time"
        elif not booking_info.seat_class:
            return "collect_seat_class"
        elif not booking_info.seat_preference:
            return "collect_seat_preference"
        else:
            return "save_to_database"


    # 定义数据库存储节点
    async def save_to_database(state: AgentState):
        booking_info = state["task_collected"]
        user_id = state["user_id"]

        # 调用数据库服务存储机票信息
        try:
            # 验证日期格式
            from datetime import datetime
            start_time = datetime.strptime(booking_info["start_time"], "%Y-%m-%d %H:%M")

            result = relative_db_service.create_flight_booking(
                user_id=user_id,
                origin=booking_info["origin"],
                destination=booking_info["destination"],
                start_time=booking_info["start_time"],
                seat_class=booking_info["seat_class"],
                seat_preference=booking_info["seat_preference"]
            )
            return {** state, "query": f"机票预订成功！您的订单已确认。预定机票信息如下："
                                                                 f"{get_list_json_str([result])}", "task_status": 2}
        except ValueError:
            return {** state, "query": "日期格式不正确，请使用YYYY-MM-DD hh:mm格式重试。", "error": "invalid_date_format", "task_status": 0}
        except Exception as e:
            return {** state, "query": f"预订失败：{str(e)}", "error": str(e), "task_status": 0}

    # 添加节点到图中
    graph.add_node("extract_info", extract_info)
    graph.add_node("collect_origin", collect_origin)
    graph.add_node("collect_destination", collect_destination)
    graph.add_node("collect_start_time", collect_start_time)
    graph.add_node("collect_seat_class", collect_seat_class)
    graph.add_node("collect_seat_preference", collect_seat_preference)
    graph.add_node("save_to_database", save_to_database)
    graph.add_node("goto_end", goto_end)
    # 设置图的入口点
    graph.set_entry_point("extract_info")

    # 添加节点之间的边
    graph.add_edge("collect_origin", END)
    graph.add_edge("collect_destination", END)
    graph.add_edge("collect_start_time", END)
    graph.add_edge("collect_seat_class", END)
    graph.add_edge("collect_seat_preference", END)
    graph.add_edge("goto_end", END)

    # 设置条件边，根据信息收集情况决定下一步
    graph.add_conditional_edges(
        "extract_info",
        should_continue,
        {
            "collect_origin": "collect_origin",
            "collect_destination": "collect_destination",
            "collect_start_time": "collect_start_time",
            "collect_seat_class": "collect_seat_class",
            "collect_seat_preference": "collect_seat_preference",
            "save_to_database": "save_to_database",
            "goto_end": "goto_end"
        }
    )

    # 设置完成点
    graph.add_edge("save_to_database", END)

    return graph