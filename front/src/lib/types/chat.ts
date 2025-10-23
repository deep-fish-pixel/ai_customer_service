// 聊天请求参数接口
export interface ChatRequest {
  message: string;
  use_rag?: boolean;
  stream?: boolean;
}

// 聊天响应接口
export interface ChatSuccessResponse {
  status: 'success';
  response: string;
}

export interface ChatFailedResponse {
  status: 'failed';
  message: string;
}

export type ChatResponse = ChatSuccessResponse | ChatFailedResponse;

// API错误类型
export interface ApiError {
  type: 'network_error' | 'timeout' | 'server_error';
  message: string;
}