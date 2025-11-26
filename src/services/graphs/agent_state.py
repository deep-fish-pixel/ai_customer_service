from typing import Dict, Any, List, Optional, Literal
from typing_extensions import TypedDict

class AgentState(TypedDict):
    task_status: int
    user_id: str
    query: str
    task_type: str
    history: List[Any]
    task_collected: dict
    task_extra: Optional[Dict[str, Any]] = None
    res_type: str
    res_value: str
    exit: int
