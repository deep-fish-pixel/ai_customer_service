from src.enums.Status import Status
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from src.utils.json import json_stringfy
from src.enums.JsonSeperator import JsonSeperator
import re

#预定酒店表
class HotelBookingTable(Status):
  ID = ('id', "id")
  CITY = ('city', "城市")
  CHECKIN_DATE = ('checkin_date', "入住日期")
  CHECKOUT_DATE = ('checkout_date', "退房日期")
  ROOM_TYPE = ('room_type', "房型")
  GUEST_COUNT = ('guest_count', "人数")

  # 验证值是否合法
  @staticmethod
  def valide_value(column: str, new_value: any, record: Dict[str, Any]):
    if(column == HotelBookingTable.CHECKOUT_DATE.value):
      checkin = datetime.strptime(record["checkin_date"], "%Y-%m-%d").replace(hour=12, minute=0, second=0)
      checkout = datetime.strptime(new_value, "%Y-%m-%d").replace(hour=12, minute=0, second=0)
      if checkout <= checkin:
        return '退房日期必须晚于入住日期'
    return None

  # 获取处理后的新值
  @staticmethod
  def handle_value(column: str, new_value: any, record: Dict[str, Any]):
    if(column == HotelBookingTable.CHECKOUT_DATE.value):
      checkout = datetime.strptime(new_value, "%Y-%m-%d").replace(hour=12, minute=0, second=0)
      return checkout
    elif(column == HotelBookingTable.GUEST_COUNT.value):
      if(isinstance(new_value, str)):
        match = re.search(r'\d+', new_value)
        # 如果找到匹配项，将其转换为整数
        if match:
          number = int(match.group())
          return number
        else:
          return 0
    return new_value

  @staticmethod
  def get_list_json_str(result: List[Dict[str, Any]]):
    """获取查询信息的展示数据"""
    dataList = [[
      HotelBookingTable.ID.text,
      HotelBookingTable.CITY.text,
      HotelBookingTable.CHECKIN_DATE.text,
      HotelBookingTable.CHECKOUT_DATE.text,
      HotelBookingTable.ROOM_TYPE.text,
      HotelBookingTable.GUEST_COUNT.text,
    ], []]
    list = dataList[1]

    for info in result:
      data = [
        info[HotelBookingTable.ID.value],
        info[HotelBookingTable.CITY.value],
        info[HotelBookingTable.CHECKIN_DATE.value].strftime("%Y-%m-%d %H:%M"),
        info[HotelBookingTable.CHECKOUT_DATE.value].strftime("%Y-%m-%d %H:%M"),
        info[HotelBookingTable.ROOM_TYPE.value],
        info[HotelBookingTable.GUEST_COUNT.value],
      ]
      list.append(data)

    return json_stringfy(dataList)



