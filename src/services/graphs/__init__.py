from langgraph.graph import StateGraph

from src.services.graphs.create_flight_booking_graph import create_flight_booking_graph
from src.services.graphs.query_flight_booking_graph import query_flight_booking_graph
from src.services.graphs.create_hotel_booking_graph import create_hotel_booking_graph
from src.services.graphs.query_hotel_booking_graph import query_hotel_booking_graph
from src.services.graphs.create_schedule_meeting_graph import create_schedule_meeting_graph
from src.services.graphs.query_schedule_meeting_graph import query_schedule_meeting_graph
from src.services.graphs.create_leave_request_graph import create_leave_request_graph
from src.services.graphs.query_leave_request_graph import query_leave_request_graph
from src.services.graphs.change_my_nickname_graph import change_my_nickname_graph
from src.services.graphs.change_list_record_property_graph import change_list_record_property_graph
from src.services.graphs.delete_list_record_graph import delete_list_record_graph
from src.services.multi_modal_graphs.text_to_image_graph import text_to_image_graph
from src.services.multi_modal_graphs.edit_image_graph import edit_image_graph
from src.services.multi_modal_graphs.text_to_video_graph import text_to_video_graph


SUPPORTED_TASKS = [
    "book_flight",
    "query_book_flight",
    "book_hotel",
    "query_book_hotel",

    "schedule_meeting",
    "query_schedule_meeting",

    "leave_request",
    "query_leave_request",

    "change_list_record_property",
    "delete_list_record",

    "change_my_nickname",

    "create_image",
    "edit_image",
    "create_video",
]

task_graphs = {
    "book_flight": create_flight_booking_graph,
    "query_book_flight": query_flight_booking_graph,

    "book_hotel": create_hotel_booking_graph,
    "query_book_hotel": query_hotel_booking_graph,

    "schedule_meeting": create_schedule_meeting_graph,
    "query_schedule_meeting": query_schedule_meeting_graph,

    "leave_request": create_leave_request_graph,
    "query_leave_request": query_leave_request_graph,

    "change_list_record_property": change_list_record_property_graph,
    "delete_list_record": delete_list_record_graph,

    "change_my_nickname": change_my_nickname_graph,

    "create_image": text_to_image_graph,
    "edit_image": edit_image_graph,
    "create_video": text_to_video_graph,
}

def get_task_graph(task_type: str) -> StateGraph:
    """获取特定任务类型的LangGraph"""

    if task_type not in task_graphs:
        raise ValueError(f"不支持的任务类型: {task_type}")
    return task_graphs[task_type]()