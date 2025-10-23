import type { ChatRequest, ChatResponse, ApiError } from '../types/chat';
import { request } from './apiClient';

// API基础配置
const API_BASE_URL = 'http://localhost:8000';
const CHAT_ENDPOINT = '/api/chat/invoke';
const CHAT_STREAM_ENDPOINT = '/api/chat/stream';
const USER_ID = 'test_user_001';

/**
 * 发送聊天消息到后端API（非流式）
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

/**
 * 发送聊天消息到后端API（流式）
 * @param message 用户输入的消息内容
 * @param onChunk 接收流式数据的回调函数
 * @param onComplete 流结束的回调函数
 * @param onError 错误处理的回调函数
 * @returns 取消请求的函数
 */
export function sendChatMessageStream(
  message: string,
  onChunk: (chunk: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
): () => void {
  const requestData: ChatRequest = { message };
  const abortController = new AbortController();

  // 使用fetch API处理POST流式请求
  fetch(`${API_BASE_URL}${CHAT_STREAM_ENDPOINT}?stream=true`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-Id': USER_ID
    },
    body: JSON.stringify(requestData),
    signal: abortController.signal
  })
    .then(response => {
        debugger
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No readable stream');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      // 递归读取流数据
      const readChunk = () => {
        reader.read()
          .then(({ done, value }) => {
              debugger
            if (done) {
              // 处理剩余缓冲区数据
              if (buffer.trim()) {
                  debugger
                onChunk(buffer.trim());
              }
              onComplete();
              return;
            }

            if (value) {
              buffer += decoder.decode(value, { stream: true });
              // 按行分割数据
              const lines = buffer.split('\n');
              buffer = lines.pop() || '';

              lines.forEach(line => {
                // 移除SSE数据前缀
                const data = line.replace(/^data: /, '').trim();
                if (data) {
                  onChunk(data);
                }
              });
            }

            readChunk();
          })
          .catch(error => {
            onError(error);
          });
      };

      readChunk();
    })
    .catch(error => {
      onError(error);
    });

  // 返回取消函数
  return () => {
    abortController.abort();
  };
}