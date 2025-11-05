from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
# pip install -U langgraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END,StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
#导入tavily搜索api库
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
import os


tools =[TavilySearchResults(max_results=1)]

#1.初始化模型和工具，定义并绑定工具到模型
llm = ChatOpenAI(
    model="qwen-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
    temperature=0
)

agent_executor = create_react_agent(llm, tools)

class AssistantState(TypedDict):
    user_input: str                     # 当前用户输入
    intent: Optional[str]               # 识别出的意图（flight, hotel, leave, schedule）
    collected_params: dict              # 已收集的参数（如 {"origin": "北京", "date": "2024-05-20"}）
    required_params: List[str]          # 当前意图所需参数列表
    response: str                       # 最终回复
    needs_confirmation: bool            # 是否需要用户确认
    confirmed: bool                     # 用户是否已确认


def detect_intent(state: AssistantState) -> AssistantState:
    user_input = state["user_input"]
    # 可用 LLM 或规则判断意图
    if "机票" in user_input or "航班" in user_input:
        intent = "flight"
        required = ["origin", "destination", "date"]
    elif "酒店" in user_input:
        intent = "hotel"
        required = ["city", "check_in", "check_out"]
    elif "请假" in user_input:
        intent = "leave"
        required = ["start_date", "end_date", "reason"]
    elif "日程" in user_input or "安排" in user_input:
        intent = "schedule"
        required = ["title", "date", "time"]
    else:
        intent = "unknown"
        required = []

    return {
        **state,
        "intent": intent,
        "required_params": required,
        "collected_params": {}
    }


def collect_parameters(state: AssistantState) -> AssistantState:
    missing = [p for p in state["required_params"] if p not in state["collected_params"]]
    if not missing:
        return {**state, "needs_confirmation": True}

    # 询问第一个缺失参数（实际可用 LLM 生成自然语言）
    param = missing[0]
    question_map = {
        "origin": "请问您的出发地是？",
        "destination": "目的地是？",
        "date": "出行日期是？",
        "city": "请问您想预订哪个城市的酒店？",
        # ... 其他映射
    }
    state["response"] = question_map.get(param, f"请提供 {param}：")
    return state


def execute_action(state: AssistantState) -> AssistantState:
    intent = state["intent"]
    params = state["collected_params"]

    if intent == "flight":
        result = f"✅ 已预订机票：{params['origin']} → {params['destination']}，日期 {params['date']}"
    elif intent == "hotel":
        result = f"✅ 已预订酒店：{params['city']}，入住 {params['check_in']}"
    # ... 其他
    else:
        result = "❌ 无法处理该请求"

    return {**state, "response": result}


def parse_user_input_for_params(state: AssistantState) -> AssistantState:
    # 简化：假设用户直接提供缺失参数（实际可用 NER 或 LLM 提取）
    user_input = state["user_input"]
    current_missing = [p for p in state["required_params"] if p not in state["collected_params"]]

    # 示例：若缺 "origin"，且用户说“北京”，则填入
    if "origin" in current_missing and "北京" in user_input:
        state["collected_params"]["origin"] = "北京"
    # ... 其他逻辑（可用 LLM 结构化提取）

    return state


def should_collect_more(state: AssistantState) -> str:
    missing = [p for p in state["required_params"] if p not in state["collected_params"]]
    if missing:
        return "collect_parameters"
    elif state.get("needs_confirmation", False) and not state.get("confirmed", False):
        return "ask_for_confirmation"
    else:
        return "execute_action"

def should_confirm(state: AssistantState) -> str:
    return "execute_action" if state.get("confirmed") else "collect_parameters"

def action(state: AssistantState):
    messages = state['response']
    response = llm.invoke(messages)
    return {
        'messages': [response]
    }

workflow = StateGraph(AssistantState)

# 添加节点
workflow.add_node("detect_intent", detect_intent)
workflow.add_node("collect_parameters", collect_parameters)
workflow.add_node("parse_input", parse_user_input_for_params)
workflow.add_node("execute_action", execute_action)
# workflow.add_node("agent", action)

# 设置入口
workflow.set_entry_point("detect_intent")

# 添加边
workflow.add_edge("detect_intent", "collect_parameters")
workflow.add_edge("collect_parameters", "parse_input")
workflow.add_conditional_edges(
    "collect_parameters",
    should_collect_more,
    {
        "collect_parameters": "collect_parameters",
        "execute_action": "execute_action"
    }
)
workflow.add_edge("execute_action", END)


app = workflow.compile()

#将生成的图片保存到文件
graph_png = app.get_graph().draw_mermaid_png()

with open("lang-graph.png", "wb") as f:
    f.write(graph_png)

state = app.invoke({
    "user_input": "我想订机票",
    "collected_params": {},
    "confirmed": False
}, config={"recursion_limit": 50})
# state = app.invoke(
#     {'messages': [HumanMessage(content='我想订机票')],}
# )
