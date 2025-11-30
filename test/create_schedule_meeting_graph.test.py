import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.graphs import get_task_graph
import asyncio

task_type = "schedule_meeting"

graph = get_task_graph(task_type)

input_data = {
    "user_id": '1',
    # "query": '帮我定个日程会议',
    "query": '帮我定个日程，会议标题是讨论一下人生，日程类型是会议，会议类型是线下会议，开始时间是2020-10-10 10:00，会议时长是1小时，会议室名称是东游，参与者张三和马丽',
    # "query": '帮我定个日程，会议标题是我需要思考。日程的具体类型是专注时间，专注时间2020-10-10 10:00，专注时长2小时',
    # "query": '帮我定个日程，会议标题是我需要思考。日程的具体类型是私人事务，专注时间2020-10-10 10:00，专注时长2小时',
    "history": ['您好！我是小智，您的智能助手，有什么可以帮助您的吗？'],
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

    user_answer = 'Test response'  # Automated response for testing

    input_data['history'].append(input_data['query'])
    input_data['query'] = user_answer
    result2 = await app.ainvoke(input_data)
    print(result2)


asyncio.run(invoke())