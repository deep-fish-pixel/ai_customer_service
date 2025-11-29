import {escapeRegex} from "./lib/utils/regex";
import type {ModelType} from "./lib/types";

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
  CALL_GET_USER_INFO: "__Call__[Method]__[", //完整数据格式：__Call__[Method]__[getUserinfo, []]
  // 方法调用
  CALL_GET_IMAGE_TASKS: "__Call__[Method]__["
}

// 特殊功能分隔符正则
export const JsonSeperatorRegex = {
  // 表格类型展示
  TYPE_LIST: new RegExp(escapeRegex(JsonSeperator.TYPE_LIST)),
  // 方法调用
  CALL_GET_USER_INFO: new RegExp(escapeRegex(JsonSeperator.CALL_GET_USER_INFO) + '(\\S+),\\s*(\[[\\s\\S]*])]')
}

// 对JsonSeperator下所有正则的拼接
export const JsonSeperatorRegexJoinings = new RegExp(`(${escapeRegex(JsonSeperator.TYPE_LIST)}|${escapeRegex(JsonSeperator.CALL_GET_USER_INFO)})`);


// 多模态类型
export const ModelTypes = {
  Text: {
    value: 'text' as ModelType,
    lable: '文本对话',
    taskType: '',
  },
  Image: {
    value: 'image' as ModelType,
    lable: '图片生成',
    taskType: 'create_image',
  },
  ImageEdit: {
    value: 'image' as ModelType,
    lable: '图片编辑',
    taskType: 'edit_image',
  },
  Video: {
    value: 'video' as ModelType,
    lable: '视频生成',
    taskType: 'create_video',
  },
}

// 数据展示格式
export const DataShowTypes = {
  Table: {
    value: 'table',
    lable: '表格',
  },
  Images: {
    value: 'images',
    lable: '图片列表',
  },
  Videos: {
    value: 'videos',
    lable: '图片列表',
  },
}

// 图片比例
export const ImageRatioTypes = {
  '16:9': {
    size: '1664*928',
    style: [16, 9].map(value => value * 15),
  },
  '4:3': {
    size: '1472*1140',
    style: [4, 3].map(value => value * 60),
  },
  '1:1': {
    size: '1328*1328',
    style: [1, 1].map(value => value * 240),
  },
  '3:4': {
    size: '1140*1472',
    style: [3, 4].map(value => value * 80),
  },
  '9:16': {
    size: '928*1664',
    style: [9, 16].map(value => value * 25),
  },
};

// 视频比例
export const VideoRatioTypes = {
  '16:9': {
    size: '832*480',
    style: [16, 9].map(value => value * 25),
  },
  '1:1': {
    size: '624*624',
    style: [1, 1].map(value => value * 400),
  },
  '9:16': {
    size: '480*832',
    style: [9, 16].map(value => value * 44),
  },
};



