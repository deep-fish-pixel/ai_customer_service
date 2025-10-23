import type { ChatRequest, Response, ApiError } from '../types/chat';
import { request } from './apiClient';
import type { Message, } from "../types/chat";
import {API_BASE_URL} from "../../constants";

// API基础配置
const CHAT_ENDPOINT = `${API_BASE_URL}/api/chat/invoke`;
const CHAT_STREAM_ENDPOINT = `${API_BASE_URL}/api/chat/stream`;
const USER_ID = 'test_user_001';

/**
 * 发送聊天消息到后端API（非流式）
 * @param message 用户输入的消息内容
 * @param history 历史消息列表
 * @returns 聊天响应或错误信息
 */
export async function sendChatMessage(message: string, history: Array<Message> = []): Promise<Response<any>> {
  const requestData: ChatRequest = { message,  history };

  return request<Response<any>>(`${CHAT_ENDPOINT}`, {
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
 * @param history 历史消息列表
 * @param onChunk 接收流式数据的回调函数
 * @param onComplete 流结束的回调函数
 * @param onError 错误处理的回调函数
 * @returns 取消请求的函数
 */
export function sendChatMessageStream(
  message: string,
  history: Array<Message> = [],
  onChunk: (chunk: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
): () => void {
  const requestData: ChatRequest = { message, history, stream: true };
  const abortController = new AbortController();

  // 使用fetch API处理POST流式请求
  fetch(`${CHAT_STREAM_ENDPOINT}?stream=true`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-Id': USER_ID
    },
    body: JSON.stringify(requestData),
    signal: abortController.signal
  })
    .then(response => {
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
            if (done) {
              // 处理剩余缓冲区数据
              // 解析SSE格式数据
              const events = buffer.split('\n\n');
              buffer = events.pop() || ''; // 保留不完整的最后一个事件

              for (const event of events) {
                if (event.startsWith('data: ')) {
                  const data = event.slice(6).trim();
                  if (data) {
                    try {
                      // 解析JSON数据并提取内容
                      const parsed = JSON.parse(data);
                      // 检查JSON内容中是否包含协程对象
                      // 检查整个JSON对象是否包含协程对象
                      if (JSON.stringify(parsed).includes('coroutine object')) {
                        onError(new Error('后端返回未执行的协程对象，请检查服务端实现'));
                      } else {
                        onChunk(parsed.content || parsed.response || data);
                      }
                    } catch (e) {
                       // 检测协程对象错误并触发错误处理
                       // 使用正则表达式检测任何协程对象格式
                       if (/<coroutine object [^>]+>/.test(data)) {
                         onError(new Error('后端返回未执行的协程对象，请检查服务端实现'));
                       } else {
                         // 非JSON格式直接传递
                         onChunk(data);
                       }
                     }
                  }
                }
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