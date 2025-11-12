from src.enums.AgentEntity import AgentEntity, AgentEntityTable


def getUpdateTableColumn(table_desc: str, column_desc: str):
  """更新表的字段的sql"""
  table_name = AgentEntity.get_value_by_text(table_desc)
  table_info = AgentEntityTable.get_text_by_value(table_name)

  if (table_name and table_info):
    column = table_info.get_value_by_text(column_desc)

    if(column):
      return f"UPDATE {table_name} SET {column} = %s WHERE id = %s"
  return None