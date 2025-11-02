import { request } from './apiClient';
import type { DocumentFile, DocumentListResponse } from '../types/document';
import type {ApiError, Response, } from '../types/chat';
import {API_BASE_URL} from "../../constants";
import getHeaders from "../utils/getHeaders";

const CHAT_ENDPOINT = `${API_BASE_URL}/api/documents`;

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
export async function uploadDocument(file: File, onProgress?: (progress: number) => void): Promise<DocumentFile> {
  const formData = new FormData();
  formData.append('file', file);
    // 文件上传不需要设置Content-Type，浏览器会自动添加正确的类型和边界
    const response = await request<DocumentFile>(`${CHAT_ENDPOINT}/upload`, {
      method: 'POST',
      headers: getHeaders(), //'multipart/form-data'
      body: formData,
    });

    if (isApiError(response)) {
    throw new Error(response.message || '文件上传失败');
  }

  return response.response;
}

/**
 * 获取知识库文件列表
 * @returns 文件列表数组
 */
export async function getDocumentList(): Promise<DocumentFile[]> {
  const response = await request<DocumentFile[]>(`${CHAT_ENDPOINT}`, {
    method: 'GET',
    headers: getHeaders('application/json')
  });

  if (isApiError(response)) {
    throw new Error(response.message || '获取知识库列表失败');
  }

  return response.response;
}

/**
 * 删除知识库中的文件
 * @param fileId - 要删除的文件ID
 * @returns 删除是否成功
 */
export async function deleteDocument(fileId: string): Promise<Response<string>> {
  const response = await request<string>(`${CHAT_ENDPOINT}/${fileId}`, {
    method: 'DELETE',
    headers: getHeaders('application/json')
  });

  return response;
}