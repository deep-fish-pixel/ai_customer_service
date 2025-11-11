from langgraph.graph import StateGraph, END
from src.enums.ScheduleMeeting import ScheduleMeetingType, MeetingType
from src.services.graphs.agent_state import AgentState
from src.services.relative_db_service import relative_db_service
from src.utils.json import json_stringfy
from src.enums.JsonSeperator import JsonSeperator
from typing import List, Dict, Any

def get_list_json_str(result: List[Dict[str, Any]]):
  """获取查询信息的展示数据"""
  dataList = [["id", "标题", "日程类型", "会议类型", "会议室", "日期", "会议时长", "参与者",], []]
  list = dataList[1]

  for info in result:
    data = [
      info["id"],
      info["title"],
      ScheduleMeetingType.get_text_by_value(info["type"]),
      MeetingType.get_text_by_value(info["meeting_type"]) if info["meeting_type"] else '',
      info["meeting_room"],
      info["start_time"].strftime("%Y-%m-%d %H:%M"),
      str(int((info["end_time"] - info["start_time"]).total_seconds() // 60)) + "分钟",
      info["participants"],
    ]
    list.append(data)

  return JsonSeperator.TYPE_LIST + json_stringfy(dataList)

def query_schedule_meeting_graph() -> StateGraph:
    """查询日程会议的信息工作流，收集所有必要信息并完成数据库存储"""
    graph = StateGraph(AgentState)

    # 定义信息提取和验证函数
    async def query(state: AgentState) -> AgentState:
        result = relative_db_service.list_schedule_meetings(state['user_id'])

        query = '已查询到您的日程会议记录：'
        return {** state, "task_response": 2, "query": query + get_list_json_str(result)}

    # 添加节点到图中
    graph.add_node("query", query)
    # 设置图的入口点
    graph.set_entry_point("query")
    graph.add_edge("query", END)


    return graph