// 消息接口
export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

// 聊天请求参数接口
export interface ChatRequest {
  message: string;
  use_rag?: boolean;
  stream?: boolean;
  history?: Array<Message>
}

// API错误类型
export interface ApiError {
  type: 'network_error' | 'timeout' | 'server_error';
  status: 'failed';
  message: string;
}

export interface Response<T> {
  status: 'success' | 'failed';
  response?: T;
  message?: string;
}