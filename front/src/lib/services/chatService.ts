import type { ChatRequest, ChatResponse, ApiError } from '../types/chat';
import { request } from './apiClient';

// API基础配置
const API_BASE_URL = 'http://localhost:8000';
const CHAT_ENDPOINT = '/api/chat/invoke';
const USER_ID = 'test_user_001';

/**
 * 发送聊天消息到后端API
 * @param message 用户输入的消息内容
 * @returns 聊天响应或错误信息
 */
export async function sendChatMessage(message: string): Promise<ChatResponse | ApiError> {
  const requestData: ChatRequest = { message };

  return request<ChatResponse>(`${API_BASE_URL}${CHAT_ENDPOINT}`, {
    method: 'POST',
    headers: {
      'X-User-Id': USER_ID
    },
    body: JSON.stringify(requestData),
    timeout: 30000
  });
}