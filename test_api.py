import requests
import json
import os
from requests_toolbelt import MultipartEncoder

# 基本配置
BASE_URL = "http://localhost:8000"
USER_ID = "test_user_001"
HEADERS = {
    "X-User-Id": USER_ID,
    "Content-Type": "application/json"
}

def test_health_check():
    """测试健康检查接口"""
    print("=== 测试健康检查接口 ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_simple_chat():
    """测试简单聊天接口"""
    print("=== 测试简单聊天接口 ===")
    data = {
        "message": "你好，小智！",
        "use_rag": False
    }
    response = requests.post(f"{BASE_URL}/api/chat/send", headers=HEADERS, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_rag_chat():
    """测试简单聊天接口"""
    print("=== 测试RAG聊天接口 ===")
    data = {
        "message": "如何创建一个应用？",
        "use_rag": True
    }
    response = requests.post(f"{BASE_URL}/api/chat/send", headers=HEADERS, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


def test_upload():
    # test_upload_rag()
    test_rag_chat()

def test_upload_rag():
    """测试上传RAG接口"""
    print("=== 测试RAG聊天接口 ===")

    file = open('./resources/create_app.pdf', 'rb')
    m = MultipartEncoder(
        fields={
            'file': ('create_app.pdf', file, 'application/pdf')
        }
    )
    response = requests.post(
        f"{BASE_URL}/api/documents/upload",
        headers={**HEADERS, 'Content-Type': m.content_type},
        data=m
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()


def test_leave_request():
    """测试请假申请接口"""
    print("=== 测试请假申请接口 ===")
    data = {
        "request_text": "我需要请年假，从2024年6月1日到6月3日，共3天，因为家里有事需要处理。"
    }
    response = requests.post(f"{BASE_URL}/api/agent/leave", headers=HEADERS, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_meeting_request():
    """测试会议预约接口"""
    print("=== 测试会议预约接口 ===")
    data = {
        "request_text": "请帮我预约一个产品讨论会，时间是2024年6月10日下午2点，时长60分钟，参会人员有张三、李四、王五，地点在会议室A，会议议程是讨论新产品功能规划。"
    }
    response = requests.post(f"{BASE_URL}/api/agent/meeting", headers=HEADERS, json=data)
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")
    print()

def test_get_records():
    """测试获取记录接口"""
    print("=== 测试获取请假记录接口 ===")
    response = requests.get(f"{BASE_URL}/api/agent/leave/records", headers=HEADERS)
    print(f"状态码: {response.status_code}")
    print(f"请假记录: {response.json()}")
    print()
    
    print("=== 测试获取会议记录接口 ===")
    response = requests.get(f"{BASE_URL}/api/agent/meeting/records", headers=HEADERS)
    print(f"状态码: {response.status_code}")
    print(f"会议记录: {response.json()}")
    print()

if __name__ == "__main__":
    print("开始测试API接口...")
    print(f"测试用户ID: {USER_ID}")
    print()
    
    # 注意：在运行这些测试之前，请确保服务已经启动
    # 并且已经正确配置了OpenAI API密钥
    
    test_health_check()
    
    # 以下测试需要服务运行并且有正确的API密钥
    # 请根据实际情况选择性运行
    try:
        test_upload()
        # test_simple_chat()
        # test_leave_request()
        # test_meeting_request()
        # test_get_records()
        print("所有测试完成！")
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        print("请确保服务已经启动并且正确配置了API密钥。")