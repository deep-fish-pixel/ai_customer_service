import json
from datetime import datetime

# 自定义序列化函数
def json_serializer(obj):
  if isinstance(obj, datetime):
    return obj.isoformat()  # 或者用 str(obj)、obj.strftime(...) 等格式
  raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

# 把对象字符串化
def json_stringfy(data: any):
  return json.dumps(data, default=json_serializer, ensure_ascii=False)