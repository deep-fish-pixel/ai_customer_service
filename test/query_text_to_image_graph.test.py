import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.graphs import get_task_graph
import asyncio

task_type = "create_image"

graph = get_task_graph(task_type)

input_data = {
    "user_id": '1',
    "query": '一只小猫玩耍',
    "history": [],
    "context": [],
    "task_collected": {},
    "task_type":"text_to_image",
    "task_extra": {
        "size": "1328*1328",
        "n": 3,
    },
}

app = graph.compile()

async def invoke():
    result = await app.ainvoke(input_data)
    print("invoke=========", result)

asyncio.run(invoke())