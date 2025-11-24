from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Dict, Any, List
from pydantic import BaseModel

from src import RESPONSE_STATUS_FAILED, RESPONSE_STATUS_SUCCESS
from src.api.endpoints import get_user_id
from dashscope import ImageSynthesis
import os
from http import HTTPStatus

# 创建路由器
router = APIRouter()

# 定义请求模型
class QueryTaskRequest(BaseModel):
  task_id: str


api_key = os.getenv("DASHSCOPE_API_KEY")


@router.get("/image_tasks/{task_id}", response_model=Dict[str, Any])
def query_image_task(
  task_id: str,
  # user_id: str = Depends(get_user_id)
) -> Dict[str, Any]:
  """
  查询任务进度

  Args:
      request: 任务请求
      user_id: 用户ID

  Returns:
      处理结果
  """
  try:
    status_rsp = ImageSynthesis.fetch(
      task=task_id,
      api_key=api_key
    )

    if status_rsp.status_code != HTTPStatus.OK:
      print(
        f'获取任务状态失败, status_code: {status_rsp.status_code}, code: {status_rsp.code}, message: {status_rsp.message}')
      return {
          "status": RESPONSE_STATUS_FAILED,
          "message": "查询任务状态失败",
          "data": None
      }

    task_status = status_rsp.output.task_status
    print(f'当前任务状态: {task_status}')

    if task_status == 'SUCCEEDED':
      print('任务已完成，正在下载图像...')
      result_urls = [result.url for result in status_rsp.output.results]
      return {
        "status": RESPONSE_STATUS_SUCCESS,
        "message": "查询成功",
        "data": {
          "list": result_urls,
          "process": task_status
        }
      }
    elif task_status == 'FAILED':
      print(f'任务执行失败, status: {task_status}, code: {status_rsp.code}, message: {status_rsp.message}')
      return {
          "status": RESPONSE_STATUS_SUCCESS,
          "message": f'任务执行失败, status: {task_status}, code: {status_rsp.code}, message: {status_rsp.message}',
          "data": {
              "list": [],
              "process": task_status,
          }
      }
    elif task_status == 'PENDING' or task_status == 'RUNNING':
      print('任务正在进行中，5秒后继续查询...')
      return {
          "status": RESPONSE_STATUS_SUCCESS,
          "message": "任务正在进行中，5秒后继续查询...",
          "data": {
              "list": [],
              "process": task_status,
          }
      }
    elif task_status == 'CANCELED':
      print('任务取消')
      return {
          "status": RESPONSE_STATUS_SUCCESS,
          "message": "任务取消",
          "data": {
              "list": [],
              "process": task_status,
          }
      }
    else:
      print(f'未知任务状态: {task_status}，5秒后继续查询...')
      return {
          "status": RESPONSE_STATUS_SUCCESS,
          "message": f'未知任务状态: {task_status}，5秒后继续查询...',
          "data": {
              "list": [],
              "process": task_status,
          }
      }
  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
