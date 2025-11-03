
import getUserId from "./getUserId";

/**
 * 创建基础请求头
 * @param contentType
 */
export default function (contentType?: string) {
    const headers: Record<string, string> = {
        'X-User-ID': getUserId()
    };

    if (contentType) {
        headers['Content-Type'] = contentType;
    }

    return headers;
};