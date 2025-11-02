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
