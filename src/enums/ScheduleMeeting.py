from src.enums.Status import Status

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
