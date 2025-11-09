from langgraph.graph import StateGraph

from src.services.graphs.create_flight_booking_graph import create_flight_booking_graph
from src.services.graphs.query_flight_booking_graph import query_flight_booking_graph
from src.services.graphs.create_hotel_booking_graph import create_hotel_booking_graph
from src.services.graphs.query_hotel_booking_graph import query_hotel_booking_graph
from src.services.graphs.create_schedule_meeting_graph import create_schedule_meeting_graph
from src.services.graphs.query_schedule_meeting_graph import query_schedule_meeting_graph
from src.services.graphs.create_leave_request_graph import create_leave_request_graph
from src.services.graphs.query_leave_request_graph import query_leave_request_graph

from src.services.graphs.create_personal_info_graph import create_personal_info_graph



SUPPORTED_TASKS = [
    "book_flight",
    "query_book_flight",
    "book_hotel",
    "query_book_hotel",

    "schedule_meeting",
    "query_schedule_meeting",

    "request_leave",
    "query_request_leave",

    "check_personal_info"
]

task_graphs = {
    "book_flight": create_flight_booking_graph,
    "query_book_flight": query_flight_booking_graph,

    "book_hotel": create_hotel_booking_graph,
    "query_book_hotel": query_hotel_booking_graph,

    "schedule_meeting": create_schedule_meeting_graph,
    "query_schedule_meeting": query_schedule_meeting_graph,

    "request_leave": create_leave_request_graph,
    "query_request_leave": query_leave_request_graph,

    "check_personal_info": create_personal_info_graph
}

def get_task_graph(task_type: str) -> StateGraph:
    """获取特定任务类型的LangGraph"""

    if task_type not in task_graphs:
        raise ValueError(f"不支持的任务类型: {task_type}")
    return task_graphs[task_type]()