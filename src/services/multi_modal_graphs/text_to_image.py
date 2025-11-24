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


class HotelBookingInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0

def query_hotel_booking_graph() -> StateGraph:
    """查询酒店预订的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)
    api_key = os.getenv("DASHSCOPE_API_KEY")

    def create_async_task(state: AgentState):
        rsp = ImageSynthesis.async_call(api_key=api_key,
                                        model="qwen-image-plus",
                                        prompt=state["query"],
                                        n=1,
                                        size='1328*1328',
                                        # ref_img="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png",
                                        prompt_extend=True,
                                        watermark=False)
        print(rsp)
        if rsp.status_code == HTTPStatus.OK:
            print(rsp.output)
        else:
            print(f'创建任务失败, status_code: {rsp.status_code}, code: {rsp.code}, message: {rsp.message}')
        return rsp


    # 添加节点到图中
    graph.add_node("create_async_task", create_async_task)
    # 设置图的入口点
    graph.set_entry_point("create_async_task")
    graph.add_edge("create_async_task", END)


    return graph