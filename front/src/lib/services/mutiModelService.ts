import { request } from './apiClient';
import {API_BASE_URL} from "../../constants";
import getHeaders from "../utils/getHeaders";
import type {Response} from '../types/request';
import type {User, UserLoginRequest, UserRegisterRequest} from "../types/user";

// API基础配置
const MUTI_MODEL_ENDPOINT = `${API_BASE_URL}/api/model`;

/**
 * 获取异步生成图片的进度信息
 * @param task_id 任务id
 * @returns 任务信息
 */
export async function getImageTask(task_id: string): Promise<Response<any>> {
  return request<any>(`${MUTI_MODEL_ENDPOINT}/image_tasks/${task_id}`, {
    method: 'GET',
    headers: getHeaders('application/json'),
    timeout: 10000
  });
}
