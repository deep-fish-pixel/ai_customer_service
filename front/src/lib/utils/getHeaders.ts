import { getUserId } from "./getUser";
import {getTokenAuthorization} from "./authorization";

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

    Object.assign(headers, getTokenAuthorization());

    return headers;
};