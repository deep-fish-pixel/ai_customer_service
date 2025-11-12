from src.enums.Status import Status

#预定酒店表
class HotelBookingTable(Status):
  ID = ('id', "id")
  CITY = ('city', "城市")
  CHECKIN_DATE = ('checkin_date', "入住日期")
  CHECKOUT_DATE = ('checkout_date', "退房日期")
  ROOM_TYPE = ('room_type', "房型")
  GUEST_COUNT = ('guest_count', "人数")

