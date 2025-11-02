from typing import TypedDict, Union, Dict, Any

# src包初始化文件
# 定义两个常量字符串
RESPONSE_STATUS_SUCCESS = "success"
RESPONSE_STATUS_FAILED = "failed"

class Response(TypedDict):
    # status: Union[RESPONSE_STATUS_SUCCESS, RESPONSE_STATUS_FAILED]
    status: str
    message: Union[str, None]
    response: Any

