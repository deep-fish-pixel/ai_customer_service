from typing import TypedDict, Dict, Any, List, Optional, Literal

class AgentState(TypedDict):
    # messages: List[str]          # 对话历史
    # intent: Optional[str]        # 识别出的意图
    # params: dict                 # 当前任务所需参数（如出发地、日期等）
    # response: Optional[str]      # 最终回复
    user_id: str
    query: str
    task_type: str
    history: []
