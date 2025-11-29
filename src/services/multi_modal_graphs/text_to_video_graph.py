from langgraph.graph import StateGraph, END
from pydantic import BaseModel
import json
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getVideoHistoryAndNextChat
from typing import List, Dict, Any, Optional
from http import HTTPStatus
from dashscope import VideoSynthesis, MultiModalConversation
import os


api_key = os.getenv("DASHSCOPE_API_KEY")

class HotelBookingInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0

def text_to_video_graph() -> StateGraph:
    """文本生成图像的信息工作流"""
    graph = StateGraph(AgentState)

    async def create_async_task(state: AgentState):
      task_extra = state.get("task_extra", {
        "style": "",
        "size": "1328*1328",
        "n": 1,
      })
      query = state.get("query", "")
      size = task_extra.get("size", "624*624")
      duration = task_extra.get("duration", 5)
      rsps = []

      response = await getVideoHistoryAndNextChat("已为您生成视频", state['history'][-1], query)

      rsp = VideoSynthesis.async_call(api_key=api_key,
                                      model='wan2.5-t2v-preview',
                                      prompt=response.content,
                                      size=size,
                                      #图生视频首帧
                                      # resolution="480P",
                                      # img_url="img_url",
                                      #图生视频首尾帧
                                      # resolution="480P",
                                      # first_frame_url="first_frame_url",
                                      # last_frame_url="last_frame_url",
                                      duration=duration,
                                      negative_prompt="",
                                      audio=True,
                                      prompt_extend=True,
                                      watermark=False,
                                      seed=12345)
      if rsp.status_code == HTTPStatus.OK:
        rsps.append(rsp["output"])

      if len(rsps) > 0:
        return {
          ** state,
          "query": response.content,
          "data_type": 'images',
          "data_value": json.dumps(rsps, ensure_ascii=False),
          "task_status": 2,
        }
      else:
        return {** state, "task_status": 2, "query": "请求失败，稍后再重试一次"}

    # 添加节点到图中
    graph.add_node("create_async_task", create_async_task)
    # 设置图的入口点
    graph.set_entry_point("create_async_task")
    graph.add_edge("create_async_task", END)


    return graph