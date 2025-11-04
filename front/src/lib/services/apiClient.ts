import {showToast} from "../utils/toast";
import type {Response} from "../types/request";
import {RESPONSE_STATUS_FAILED, RESPONSE_STATUS_FAILED_TOKEN_INVALID,} from "../../constants";

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
): Promise<Response<T>> {
  const { timeout = 10000, headers = {}, ...restOptions } = options;

  // 默认请求头
  const defaultHeaders = {
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
        status: response.status === 401 ? RESPONSE_STATUS_FAILED_TOKEN_INVALID : RESPONSE_STATUS_FAILED,
        data: null as any,
        message: `服务器错误: ${response.status} ${response.statusText}`
      };
    }

    const data: Response<T> = await response.json();

    if(data.status === RESPONSE_STATUS_FAILED && data?.message) {
      showToast(data.message);
    }

    return data;
  } catch (error: unknown) {
    clearTimeout(timeoutId);

    if (typeof error === 'object' && error !== null && 'name' in error && error.name === 'AbortError') {
      return {
        status: RESPONSE_STATUS_FAILED,
        data: null as any,
        message: '请求超时，请稍后重试'
      };
    }

    return {
      status: RESPONSE_STATUS_FAILED,
      data: null as any,
      message: '网络连接错误，请检查是否正常启用: python main.py'
    };
  }
}