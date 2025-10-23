/**
 * 知识库文件类型定义
 */
export interface DocumentFile {
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
export interface DocumentListResponse {
  /** 文件列表 */
  files: DocumentFile[];
  /** 总数 */
  total: number;
  /** 当前页码 */
  page: number;
  /** 每页数量 */
  pageSize: number;
}
