// 消息接口
export interface Message {
  id: string;
  // 内容
  content: string;
  // 发送消息的角色
  sender: 'user' | 'bot';
  // 时间戳
  timestamp: Date;
  // 任务状态
  task_status?: number;
}

// 聊天请求参数接口
export interface ChatRequest {
  // 消息
  message: string;
  // 启用rag
  use_rag?: boolean;
  // 启用stream
  stream?: boolean;
  // 任务类型
  task_type?: string;
  // 任务更多配置
  task_extra?: any;
  // 历史消息
  history?: Array<Message>
}