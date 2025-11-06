from src.services.graphs import get_task_graph
import asyncio

task_type = "book_flight"

graph = get_task_graph(task_type)

input_data = {
    "user_id": '1',
    "query": '帮我定从南京飞往北京的机票',
    "history": [],
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