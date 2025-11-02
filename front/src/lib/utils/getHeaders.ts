
import getSpaceId from "./getSpaceId";

/**
 * 创建基础请求头
 * @param contentType
 */
export default function (contentType?: string) {
    const headers: Record<string, string> = {
        'X-User-ID': getSpaceId()
    };

    if (contentType) {
        headers['Content-Type'] = contentType;
    }

    return headers;
};