from src.enums.Status import Status

#预定机票表
class FlightBookingTable(Status):
  ID = ('id', "id")
  ORIGIN = ('origin', "始发地")
  DESTINATION = ('destination', "目的地")
  START_TIME = ('start_date', "开始时间")
  SEAT_CLASS = ('seat_class', "座位等级")
  SEAT_PREFERENCE = ('seat_preference', "座位偏好")


