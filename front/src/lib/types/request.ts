// API错误类型
import {RESPONSE_STATUS_FAILED, RESPONSE_STATUS_SUCCESS } from "../../constants";

export interface ApiError {
    type: 'network_error' | 'timeout' | 'server_error';
    status: 'failed';
    message: string;
}

// 请求返回内容
export interface Response<T> {
    status: typeof RESPONSE_STATUS_SUCCESS | typeof RESPONSE_STATUS_FAILED;
    data: T;
    message: string;
}