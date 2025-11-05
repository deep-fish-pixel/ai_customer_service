from src.services.graphs import get_task_graph
import asyncio

task_type = "book_flight"

graph = get_task_graph(task_type)

input_data = {
    "user_id": '1',
    "query": '定机票',
    "history": [],
    "context": []
}

app = graph.compile()

async def invoke():
    result = await app.ainvoke(input_data)
    print(result)

asyncio.run(invoke())