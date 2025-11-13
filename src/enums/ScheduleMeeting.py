from src.enums.Status import Status
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from src.utils.json import json_stringfy
from src.enums.JsonSeperator import JsonSeperator

#日程会议表
class ScheduleMeetingTable(Status):
  ID = ('id', "id")
  TITLE = ('title', "标题")
  TYPE = ('type', "日程类型")
  MEETING_TYPE = ('meeting_type', "会议类型")
  MEETING_ROOM = ('meeting_room', "会议室")
  START_TIME = ('start_time', "日期")
  END_TIME = ('end_time', "会议时长")
  PARTICIPANTS = ('participants', "参与者")

  # 验证值是否合法
  @staticmethod
  def valide_value(column: str, new_value: any, record: Dict[str, Any]|None):
    return None

  # 获取处理后的新值
  @staticmethod
  def handle_value(column: str, new_value: any, record: Dict[str, Any]):
    if(column == ScheduleMeetingTable.MEETING_TYPE.value):
      return MeetingType.get_value_by_text(new_value)
    elif(column == ScheduleMeetingTable.START_TIME.value):
      start_time = record[ScheduleMeetingTable.START_TIME.value]
      end_time = start_time+  timedelta(minutes=new_value)
      return end_time
    return new_value

  @staticmethod
  def get_list_json_str(result: List[Dict[str, Any]]):
    """获取查询信息的展示数据"""
    dataList = [[
      ScheduleMeetingTable.ID.text,
      ScheduleMeetingTable.TITLE.text,
      ScheduleMeetingTable.TYPE.text,
      ScheduleMeetingTable.MEETING_TYPE.text,
      ScheduleMeetingTable.MEETING_ROOM.text,
      ScheduleMeetingTable.START_TIME.text,
      ScheduleMeetingTable.END_TIME.text,
      ScheduleMeetingTable.PARTICIPANTS.text,
    ], []]
    list = dataList[1]

    for info in result:
      data = [
        info[ScheduleMeetingTable.ID.value],
        info[ScheduleMeetingTable.TITLE.value],
        ScheduleMeetingType.get_text_by_value(info[ScheduleMeetingTable.TYPE.value]),
        MeetingType.get_text_by_value(info[ScheduleMeetingTable.MEETING_TYPE.value]) if info[ScheduleMeetingTable.MEETING_TYPE.value] else '',
        info[ScheduleMeetingTable.MEETING_ROOM.value],
        info[ScheduleMeetingTable.START_TIME.value].strftime("%Y-%m-%d %H:%M"),
        str(int((info[ScheduleMeetingTable.END_TIME.value] - info[ScheduleMeetingTable.START_TIME.value]).total_seconds() // 60)) + "分钟",
        info[ScheduleMeetingTable.PARTICIPANTS.value],
        ]
      list.append(data)

    return JsonSeperator.TYPE_LIST + json_stringfy(dataList)

# 日程类型
class ScheduleMeetingType(Status):
  MEETING = (1, "会议")
  FOCUS_TIME = (2, "专注时间")
  PRIVATE_BUSINESS = (3, "私人事务")

#会议类型
class MeetingType(Status):
  ONLINE = (1, "线上会议")
  OFFLINE = (2, "线下会议")

# print(ScheduleMeetingType.FOCUS_TIME.name)
# print(ScheduleMeetingType.FOCUS_TIME.value)
# print(ScheduleMeetingType.FOCUS_TIME.text)
# print(ScheduleMeetingType.get_value_by_text('私人事务'))
