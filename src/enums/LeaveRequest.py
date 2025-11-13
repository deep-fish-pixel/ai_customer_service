from src.enums.Status import Status
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from src.utils.json import json_stringfy
from src.enums.JsonSeperator import JsonSeperator

#请假申请表
class LeaveRequestTable(Status):
  ID = ('id', "id")
  LEAVE_TYPE = ('leave_type', "类型")
  START_TIME = ('start_time', "开始时间")
  END_TIME = ('end_time', "结束时间")
  REASON = ('reason', "原因")
  ATTACHMENTS = ('attachments', "附件")

  # 验证值是否合法
  @staticmethod
  def valide_value(column: str, new_value: any, record: Dict[str, Any]):
    if(column == LeaveRequestTable.END_TIME.value):
      start_time = record["start_time"]
      end_time = datetime.strptime(new_value, "%Y-%m-%d %H:%M")
      if end_time <= start_time:
        return '请假申请的开始时间必须晚于结束时间'
    return None

  # 获取处理后的新值
  @staticmethod
  def handle_value(column: str, new_value: any, record: Dict[str, Any]):
    return new_value

  @staticmethod
  def get_list_json_str(result: List[Dict[str, Any]]):
    """获取查询信息的展示数据"""
    dataList = [[
      LeaveRequestTable.ID.text,
      LeaveRequestTable.LEAVE_TYPE.text,
      LeaveRequestTable.START_TIME.text,
      LeaveRequestTable.END_TIME.text,
      LeaveRequestTable.REASON.text,
      LeaveRequestTable.ATTACHMENTS.text,
    ], []]
    list = dataList[1]

    for info in result:
      data = [
        info[LeaveRequestTable.ID.value],
        info[LeaveRequestTable.LEAVE_TYPE.value],
        info[LeaveRequestTable.START_TIME.value].strftime("%Y-%m-%d %H:%M"),
        info[LeaveRequestTable.END_TIME.value].strftime("%Y-%m-%d %H:%M"),
        info[LeaveRequestTable.REASON.value],
        info[LeaveRequestTable.ATTACHMENTS.value],
      ]
      list.append(data)

    return JsonSeperator.TYPE_LIST + json_stringfy(dataList)


# 请假申请类型
class LeaveRequestType(Status):
  ANNUAL_LEAVE = (1, "年假")
  SICK_LEAVE = (2, "病假")
  ABSENCE_LEAVE = (3, "事假")
  MARRIAGE_LEAVE = (4, "婚假")
  MATERNITY_LEAVE = (5, "产假")
  PATERNITY_LEAVE = (6, "陪产假")
  BEREAVEMENT_LEAVE = (7, "丧假")
  COMPENSATED_LEAVE = (8, "调休假")

