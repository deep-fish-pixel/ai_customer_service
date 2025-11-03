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