import type { ChatRequest, } from '../types/chat';
import { request } from './apiClient';
import type { Message, } from "../types/chat";
import {API_BASE_URL} from "../../constants";
import getHeaders from "../utils/getHeaders";
import type {Response} from '../types/request';
import type {UserLoginRequest, UserRegisterRequest} from "../types/user";

// API基础配置
const USER_ENDPOINT = `${API_BASE_URL}/api/user`;

/**
 * 用户注册API
 * @param params 用户注册参数
 * @returns 用户注册响应或错误信息
 */
export async function register(params: UserRegisterRequest): Promise<Response<any>> {
    return request<Response<any>>(`${USER_ENDPOINT}/register`, {
        method: 'POST',
        headers: getHeaders('application/json'),
        body: JSON.stringify(params),
        timeout: 10000
    });
}

/**
 * 用户登录API
 * @param params 用户登录参数
 * @returns 用户登录响应或错误信息
 */
export async function login(params: UserLoginRequest): Promise<Response<any>> {
    return request<Response<any>>(`${USER_ENDPOINT}/login`, {
        method: 'POST',
        headers: getHeaders('application/json'),
        body: JSON.stringify(params),
        timeout: 10000
    });
}
