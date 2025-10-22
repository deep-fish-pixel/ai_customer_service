import type { ApiError } from '../types/chat';

export interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
  timeout?: number;
}

/**
 * 通用API请求函数
 * @param url 请求URL
 * @param options 请求选项
 * @returns 响应数据或错误信息
 */
export async function request<T>(
  url: string,
  options: RequestOptions = {}
): Promise<T | ApiError> {
  const { timeout = 10000, headers = {}, ...restOptions } = options;
  
  // 默认请求头
  const defaultHeaders = {
    'Content-Type': 'application/json',
    ...headers
  };

  // 创建AbortController处理超时
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...restOptions,
      headers: defaultHeaders,
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      return {
        type: 'server_error',
        message: `服务器错误: ${response.status} ${response.statusText}`
      };
    }

    const data: T = await response.json();
    return data;
  } catch (error: unknown) {
      clearTimeout(timeoutId);
      
      if (typeof error === 'object' && error !== null && 'name' in error && error.name === 'AbortError') {
      return {
        type: 'timeout',
        message: '请求超时，请稍后重试'
      };
    }

    return {
      type: 'network_error',
      message: '网络连接错误，请检查是否正常启用: python main.py'
    };
  }
}