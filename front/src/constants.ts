import {escapeRegex} from "./lib/utils/regex";

export const API_BASE_URL = 'http://localhost:8000';
// 请求成功标识
export const RESPONSE_STATUS_SUCCESS = "success"
// 请求失败标识
export const RESPONSE_STATUS_FAILED = "failed"
// 请求失败标识
export const RESPONSE_STATUS_FAILED_TOKEN_INVALID = "token_invalid"

export const RobotPrologue = "您好！我是小智，您的智能客服助手，有什么可以帮助您的吗？";
// 特殊功能分隔符
export const JsonSeperator = {
  // 表格类型展示
  TYPE_LIST: "__Type__[List]",
  // 方法调用
  CALL_GET_USER_INFO: "__Call__[getUserinfo]"
}

// 特殊功能分隔符正则
export const JsonSeperatorRegex = {
  // 表格类型展示
  TYPE_LIST: new RegExp(escapeRegex(JsonSeperator.TYPE_LIST)),
  // 方法调用
  CALL_GET_USER_INFO: new RegExp(escapeRegex(JsonSeperator.CALL_GET_USER_INFO) + '$')
}

console.log(
  '==================',
  '已查询到您的日程会议记录：__Type__[List][["id", "标题", "日程类型", "会议类型", "会议室", "日期", "会议时长", "参与者"], [[15, "金融故事分享", "会议", "线下会议", "东区1号", "2023-09-15 14:00", "60分钟", "安娜"], [5, "我需要思考", "专注时间", "", null, "2020-10-10 10:00", "120分钟", null], [6, "我需要思考", "专注时间", "", null, "2020-10-10 10:00", "120分钟", null], [7, "我需要思考", "私人事务", "", null, "2020-10-10 10:00", "120分钟", null], [8, "我需要思考", "私人事务", "", null, "2020-10-10 10:00", "120分钟", null], [9, "讨论一下人生", "会议", "线下会议", "东游", "2020-10-10 10:00", "60分钟", "张三, 马丽"], [10, "讨论一下人生", "会议", "线下会议", "东游", "2020-10-10 10:00", "60分钟", "张三, 马丽"], [11, "讨论一下人生", "会议", "线下会议", "东游", "2020-10-10 10:00", "60分钟", "张三, 马丽"], [12, "讨论一下人生", "会议", "线下会议", "东游", "2020-10-10 10:00", "60分钟", "张三, 马丽"], [13, "讨论一下人生", "会议", "线下会议", "东游", "2020-10-10 10:00", "60分钟", "张三, 马丽"], [14, "我需要思考", "专注时间", "", null, "2020-10-10 10:00", "120分钟", null], [16, "讨论一下人生", "会议", "线下会议", "东游", "2020-10-10 10:00", "60分钟", "张三, 马丽"]]]'
    .match(JsonSeperatorRegex.TYPE_LIST)
)
