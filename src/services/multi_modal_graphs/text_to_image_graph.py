from langgraph.graph import StateGraph, END
from pydantic import BaseModel

from src.enums.HotelBooking import HotelBookingTable
from src.services.graphs.agent_state import AgentState
from src.services.relative_db_service import relative_db_service
from src.utils.json import json_stringfy
from typing import List, Dict, Any, Optional
from src.enums.JsonSeperator import JsonSeperator
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath
import requests
from dashscope import ImageSynthesis
import os
import dashscope
import time
from src.enums.LeaveRequest import LeaveRequestTable
from src.enums.JsonSeperator import JsonSeperator


api_key = os.getenv("DASHSCOPE_API_KEY")

class HotelBookingInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0

def text_to_image_graph() -> StateGraph:
    """文本生成图像的信息工作流"""
    graph = StateGraph(AgentState)

    def create_async_task(state: AgentState):
        rsp = ImageSynthesis.async_call(api_key=api_key,
                                        model="qwen-image-plus",
                                        prompt=state["query"],
                                        n=1,
                                        size='1328*1328',
                                        prompt_extend=True,
                                        watermark=False)
        print(rsp)
        if rsp.status_code == HTTPStatus.OK:
            print(rsp.output)
            return {** state, "task_status": 2, "query": "生成的图片如下：" + JsonSeperator.CALL_GET_IMAGE_TASKS}
        else:
            return {** state, "task_status": 2, "query": "请求失败，稍后再重试一次"}

    # 添加节点到图中
    graph.add_node("create_async_task", create_async_task)
    # 设置图的入口点
    graph.set_entry_point("create_async_task")
    graph.add_edge("create_async_task", END)


    return graph