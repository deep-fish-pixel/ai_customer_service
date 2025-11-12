from src.enums.Status import Status
from src.enums.FlightBooking import FlightBookingTable
from src.enums.HotelBooking import HotelBookingTable
from src.enums.LeaveRequest import LeaveRequestTable
from src.enums.ScheduleMeeting import ScheduleMeetingTable

#Agent实体
class AgentEntity(Status):
  SCHEDULE_MEETING = ('schedule_meetings', "日程会议")
  LEAVE_REQUEST = ('leave_requests', "请假申请")
  FLIGHT_BOOKING = ('flight_bookings', "预定机票")
  HOTEL_BOOKING = ('hotel_bookings', "预定酒店")

#Agent实体对应的sql表和字段
class AgentEntityTable(Status):
  SCHEDULE_MEETING = ('schedule_meetings', ScheduleMeetingTable)
  LEAVE_REQUEST = ('leave_requests', LeaveRequestTable)
  FLIGHT_BOOKING = ('flight_bookings', FlightBookingTable)
  HOTEL_BOOKING = ('hotel_bookings', HotelBookingTable)

print(AgentEntityTable.get_text_by_value(AgentEntity.get_value_by_text("日程会议")).get_value_by_text("会议类型"))