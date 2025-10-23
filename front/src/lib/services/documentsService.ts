import { request } from './apiClient';
import type { KnowledgeFile, KnowledgeListResponse } from '../types/knowledge';
import type { ApiError } from '../types/chat';
import {API_BASE_URL} from "../../constants";

const CHAT_ENDPOINT = `${API_BASE_URL}/api/documents`;
const USER_ID = 'test_user_001';

// 创建基础请求头
const getHeaders = (contentType?: string) => {
  const headers: Record<string, string> = {
    'X-User-ID': USER_ID
  };

  if (contentType) {
    headers['Content-Type'] = contentType;
  }

  return headers;
};

// 类型守卫：检查是否为ApiError
const isApiError = (response: any): response is ApiError => {
  return 'error' in response && 'message' in response;
};

/**
 * 知识库服务
 * 提供文件上传、列表获取和删除功能
 */
/**
 * 上传知识库文件
 * @param file - 要上传的文件
 * @param onProgress - 上传进度回调函数
 * @returns 上传的文件信息
 */
export async function uploadFile(file: File, onProgress?: (progress: number) => void): Promise<KnowledgeFile> {
  const formData = new FormData();
  formData.append('file', file);
    debugger

    // 文件上传不需要设置Content-Type，浏览器会自动添加正确的类型和边界
    const response = await request<KnowledgeFile | ApiError>(`${CHAT_ENDPOINT}/upload`, {
      method: 'POST',
      headers: getHeaders(), //'multipart/form-data'
      body: formData,
      onUploadProgress: (progressEvent: ProgressEvent) => {
        debugger
        if (progressEvent.lengthComputable && onProgress) {
          const progress = Math.round((progressEvent.loaded / progressEvent.total!) * 100);
          onProgress(progress);
        }
      }
    });

    if (isApiError(response)) {
    throw new Error(response.message || '文件上传失败');
  }

  return response;
}

/**
 * 获取知识库文件列表
 * @returns 文件列表数组
 */
export async function getKnowledgeList(): Promise<KnowledgeFile[]> {
  const response = await request<KnowledgeListResponse | ApiError>(`${CHAT_ENDPOINT}/list`, {
    method: 'GET',
    headers: getHeaders('application/json')
  });

  if (isApiError(response)) {
    throw new Error(response.message || '获取知识库列表失败');
  }

  if (!response || !Array.isArray(response.files)) {
    throw new Error('无效的文件列表响应格式');
  }

  // 验证每个文件项的格式
  response.files.forEach(file => {
    if (!isValidKnowledgeFile(file)) {
      throw new Error(`无效的文件信息格式: ${JSON.stringify(file)}`);
    }
  });

  return response.files;
}

/**
 * 删除知识库中的文件
 * @param fileId - 要删除的文件ID
 * @returns 删除是否成功
 */
export async function deleteFile(fileId: string): Promise<boolean> {
  const response = await request<{ success: boolean } | ApiError>(`${CHAT_ENDPOINT}/delete/${fileId}`, {
    method: 'DELETE',
    headers: getHeaders('application/json')
  });

  if (isApiError(response)) {
    throw new Error(response.message || '删除文件失败');
  }

  if (!response || response.success !== true) {
    throw new Error('删除操作未返回成功状态');
  }

  return true;
}