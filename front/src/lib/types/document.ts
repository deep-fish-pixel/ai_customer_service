/**
 * 知识库文件类型定义
 */
export interface DocumentFile {
  /** 文件名 */
  file_name: string;
  /** 文件大小(字节) */
  file_size: number;
  /** 上传时间 */
  upload_time: string;
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
