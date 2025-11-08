import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.graphs import get_task_graph
import asyncio

task_type = "leave_request"

graph = get_task_graph(task_type)

input_data = {
    "user_id": '1',
    "query": '帮我请假申请',
    "history": ['您好！我是小智，您的智能客服助手，有什么可以帮助您的吗？'],
    "context": [],
    "task_collected": {}
}

app = graph.compile()

#将生成的图片保存到文件
graph_png = app.get_graph().draw_mermaid_png()

with open(f"create_langgraph_{task_type}.png", "wb") as f:
    f.write(graph_png)

async def invoke():
    result = await app.ainvoke(input_data)
    print(result)

    user_answer = input(result['query'])

    input_data['history'].append(input_data['query'])
    input_data['query'] = user_answer
    result2 = await app.ainvoke(input_data)
    print(result2)


asyncio.run(invoke())