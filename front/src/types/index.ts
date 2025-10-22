// 文件接口定义
export interface FileItem {
  id: string;
  name: string;
  uploadTime: string;
  size: number;
}

// 工具配置接口
export interface ToolConfig {
  id: string;
  name: string;
  description: string;
  enabled: boolean;
}

// 消息接口
export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}