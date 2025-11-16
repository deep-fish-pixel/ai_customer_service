import {escapeRegex} from "./lib/utils/regex";

export const API_BASE_URL = import.meta.env.VITE_API_URL;
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

// 对JsonSeperator下所有正则的拼接
export const JsonSeperatorRegexJoinings = new RegExp(`(${escapeRegex(JsonSeperator.TYPE_LIST)}|${escapeRegex(JsonSeperator.CALL_GET_USER_INFO)})`);

