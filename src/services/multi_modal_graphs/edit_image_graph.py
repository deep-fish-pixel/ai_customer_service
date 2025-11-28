from langgraph.graph import StateGraph, END
from pydantic import BaseModel
import json
from src.services.graphs.agent_state import AgentState
from src.services.graphs.utils import getImageHistoryAndNextChat
from typing import List, Dict, Any, Optional
from http import HTTPStatus
from dashscope import ImageSynthesis, MultiModalConversation
import os


api_key = os.getenv("DASHSCOPE_API_KEY")

class HotelBookingInfo(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    date: Optional[str] = None
    seat_class: Optional[str] = None
    seat_preference: Optional[str] = None
    exit: Optional[int] = 0

def edit_image_graph() -> StateGraph:
    """文本生成图像的信息工作流"""
    graph = StateGraph(AgentState)

    async def create_async_task(state: AgentState):
      task_extra = state.get("task_extra", {
        "style": "",
        "size": "1328*1328",
        "n": 1,
      })
      query = state.get("query", "")
      style = task_extra.get("style", "")
      n = task_extra.get("n", 1)
      images = task_extra.get("images", [])
      # 随机数种子，取值范围[0,2147483647]
      seeds = [147483647, 847483647, 1847483647, ]

      query = f"{f'使用{style}风格，' if style else '' }{query}"

      response = await getImageHistoryAndNextChat("已为您编辑图片", state['history'][-1], query)
      messages = [
        {
          "role": "user",
          "content": [
            *[{"image": img} for img in images],
            {"text": response.content}
          ]
        }
      ]

      rsp = MultiModalConversation.call(
        api_key=api_key,
        model="qwen-image-edit-plus",
        messages=messages,
        stream=False,
        n=n,
        watermark=False,
        negative_prompt="",
        prompt_extend=True,
        seed=seeds[0],
        # 仅当输出图像数量n=1时支持设置size参数，否则会报错
        # size="1024*2048",
      )

      if rsp.status_code == 200:
        # 如需查看完整响应，请取消下行注释
        # print(json.dumps(rsp, ensure_ascii=False))
        # for i, content in enumerate(rsp.output.choices[0].message.content):
        #   print(f"输出图像{i+1}的URL:{content['image']}")
        return {
          **state,
          "query": response.content,
          "data_type": 'images',
          "data_value": json.dumps(rsp.output.choices[0].message.content, ensure_ascii=False),
          "task_status": 2,
        }
      else:
        return {**state, "task_status": 2, "query": "请求失败，稍后再重试一次"}

    # 添加节点到图中
    graph.add_node("create_async_task", create_async_task)
    # 设置图的入口点
    graph.set_entry_point("create_async_task")
    graph.add_edge("create_async_task", END)


    return graph