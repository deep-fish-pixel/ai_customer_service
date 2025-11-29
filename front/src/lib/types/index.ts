// 工具配置接口
export interface ToolConfig {
  id: string;
  name: string;
  description: string;
  questions: {
    question?: string;
    query?: string;
  }
}

// 模型类型
export type ModelType = 'text' | 'image' | 'video'

// 消息发送的任务更多配置
export interface TaskExtra {
  style?: string;
  size?: string;
  ratio?: string;
  n?: number;
  images: string[];
  resolution?: string;
  duration?: number;
}