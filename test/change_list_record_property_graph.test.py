import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.services.graphs import get_task_graph
import asyncio

task_type = "change_list_record_property"

graph = get_task_graph(task_type)

input_data = {
    "user_id": '1',
    # "query": '帮我把上面记录的第二条，参与者修改为李四,王五',
    # "history": ['已查询到您的日程会议记录：[{"id":5},{"id":19}]]'],
    "query": '修改第一条记录的人数为2000人',
    "history": ['已查询到您的酒店预定记录：__Type__[List][["id", "城市", "入住日期", "退房日期", "房型", "人数"], [[2, "南京", "2025-12-12 12:00", "2025-12-14 12:00", "大床房", 10], [1, "南京", "2025-12-12 12:00", "2025-12-14 12:00", "大床房", 10]]]'],
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

asyncio.run(invoke())