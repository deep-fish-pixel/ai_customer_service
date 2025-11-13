from src.enums.AgentEntity import AgentEntity, AgentEntityTable
from typing import List, Dict, Any, Optional


def get_table_info(table_desc: str):
  """获取表信息"""
  table_name = get_table_name(table_desc)
  return AgentEntityTable.get_text_by_value(table_name)

def get_table_name(table_desc: str):
  """获取表名"""
  return AgentEntity.get_value_by_text(table_desc)

def get_column_name(table_info: any, column_desc: str):
  """获取表的字段名称"""
  return table_info.get_value_by_text(column_desc)

def get_update_table_column(table_name: str, column_name: Optional[str]):
  if(table_name and column_name):
    return f"UPDATE {table_name} SET {column_name} = %s WHERE id = %s"
  return None