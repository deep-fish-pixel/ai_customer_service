from enum import Enum
from Status import Status

# 日程类型
class ScheduleMeetingType(Status):
  Meeting = (1, "会议")
  FOCUS_TIME = (2, "专注时间")
  PRIVATE_BUSINESS = (3, "私人事务")

#会议类型
class MeetingType(Status):
  ONLINE = (1, "线上会议")
  OFFLINE = (2, "线下会议")

print(ScheduleMeetingType.FOCUS_TIME.name)
print(ScheduleMeetingType.FOCUS_TIME.value)
print(ScheduleMeetingType.FOCUS_TIME.text)
