from pydantic import BaseModel
from typing import Optional, Dict, Any

class User(BaseModel):
  username: str
  password: str
  nickname: str
  token: str
  token_type: str


class CurrentUser(BaseModel):
  user: Dict[str, Any]
  user_id: int

  def __init__(self, user: Dict[str, Any], user_id: int):
    super().__init__(user=user, user_id=user_id)

current = CurrentUser({
  "username": "",
  "password": "",
  "nickname": "",
  "token": "",
  "token_type": "",
}, 123)