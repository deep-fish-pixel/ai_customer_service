from enum import Enum

class Status(Enum):
  def __init__(self, value, text):
    self._value_ = value
    self.text = text

  @classmethod
  def get_by_name(cls, name):
    """通过名称获取枚举成员"""
    try:
      return cls[name]
    except KeyError:
      return None

  @classmethod
  def get_by_value(cls, value):
    """通过值获取枚举成员"""
    for member in cls:
      if member.value == value:
        return member
    return None

  @classmethod
  def get_by_text(cls, text):
    """通过描述文本获取枚举成员"""
    for member in cls:
      if hasattr(member, 'text') and member.text == text:
        return member
    return None

  @classmethod
  def get_text_by_name(cls, name):
    """通过名称获取描述文本"""
    member = cls.get_by_name(name)
    return member.text if member else None

  @classmethod
  def get_text_by_value(cls, value):
    """通过值获取描述文本"""
    member = cls.get_by_value(value)
    return member.text if member else None

  @classmethod
  def get_value_by_text(cls, text):
    """通过描述文本获取枚举值"""
    member = cls.get_by_text(text)
    return member.value if member else None
