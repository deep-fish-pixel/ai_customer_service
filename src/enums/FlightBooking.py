from src.enums.Status import Status
from typing import List, Dict, Any, Optional
from src.utils.json import json_stringfy
from src.enums.JsonSeperator import JsonSeperator

#预定机票表
class FlightBookingTable(Status):
  ID = ('id', "id")
  ORIGIN = ('origin', "始发地")
  DESTINATION = ('destination', "目的地")
  START_TIME = ('start_time', "开始时间")
  SEAT_CLASS = ('seat_class', "座位等级")
  SEAT_PREFERENCE = ('seat_preference', "座位偏好")

  # 验证值是否合法
  @staticmethod
  def valide_value(column: str, new_value: any, record: Dict[str, Any]):
    return None

  # 获取处理后的新值
  @staticmethod
  def handle_value(column: str, new_value: any, record: Dict[str, Any]):
    return new_value

  @staticmethod
  def get_list_json_str(result: List[Dict[str, Any]]):
    """获取查询信息的展示数据"""
    dataList = [[
      FlightBookingTable.ID.text,
      FlightBookingTable.ORIGIN.text,
      FlightBookingTable.DESTINATION.text,
      FlightBookingTable.START_TIME.text,
      FlightBookingTable.SEAT_CLASS.text,
      FlightBookingTable.SEAT_PREFERENCE.text,
    ], []]
    list = dataList[1]

    for info in result:
      data = [
        info[FlightBookingTable.ID.value],
        info[FlightBookingTable.ORIGIN.value],
        info[FlightBookingTable.DESTINATION.value],
        info[FlightBookingTable.START_TIME.value].strftime("%Y-%m-%d %H:%M"),
        info[FlightBookingTable.SEAT_CLASS.value],
        info[FlightBookingTable.SEAT_PREFERENCE.value],
      ]
      list.append(data)

    return json_stringfy(dataList)