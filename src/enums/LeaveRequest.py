from src.enums.Status import Status

#请假申请表
class LeaveRequestTable(Status):
  ID = ('id', "id")
  LEAVE_TYPE = ('leave_type', "类型")
  START_TIME = ('start_time', "开始时间")
  END_TIME = ('end_time', "结束时间")
  REASON = ('reason', "原因")
  ATTACHMENTS = ('attachments', "附件")

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

