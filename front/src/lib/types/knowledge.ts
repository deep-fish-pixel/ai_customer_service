/**
 * 知识库文件类型定义
 */
export interface KnowledgeFile {
  /** 文件ID */
  id: string;
  /** 文件名 */
  name: string;
  /** 文件大小(字节) */
  size: number;
  /** 文件类型 */
  type: string;
  /** 上传时间 */
  uploadedAt: string;
  /** 文件路径 */
  path?: string;
  /** 文件状态 */
  status: 'processing' | 'ready' | 'error';
  /** 错误信息 */
  error?: string;
}

/**
 * 知识库列表响应类型
 */
export interface KnowledgeListResponse {
  /** 文件列表 */
  files: KnowledgeFile[];
  /** 总数 */
  total: number;
  /** 当前页码 */
  page: number;
  /** 每页数量 */
  pageSize: number;
}

/**
 * 知识库上传请求参数
 */
export interface UploadParams {
  /** 文件 */
  file: File;
  /** 进度回调 */
  onProgress?: (progress: number) => void;
}

/**
 * 知识库错误响应类型
 */
export interface KnowledgeErrorResponse {
  /** 错误信息 */
  message: string;
  /** 错误代码 */
  code?: string;
}