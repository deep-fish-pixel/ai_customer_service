import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from src import RESPONSE_STATUS_FAILED, RESPONSE_STATUS_SUCCESS

# 加载环境变量
load_dotenv()

# 定义请假请求模型
class LeaveRequest(BaseModel):
    employee_name: str = Field(description="员工姓名")
    leave_type: str = Field(description="请假类型")
    start_date: str = Field(description="开始日期，格式：YYYY-MM-DD")
    end_date: str = Field(description="结束日期，格式：YYYY-MM-DD")
    reason: str = Field(description="请假原因")
    duration_days: float = Field(description="请假天数")

# 定义会议预约模型
class MeetingRequest(BaseModel):
    meeting_title: str = Field(description="会议标题")
    participants: List[str] = Field(description="参会人员列表")
    meeting_time: str = Field(description="会议时间，格式：YYYY-MM-DD HH:MM")
    duration_minutes: int = Field(description="会议时长（分钟）")
    location: str = Field(description="会议地点")
    agenda: str = Field(description="会议议程")

class AgentService:
    """Agent服务类"""
    
    def __init__(self):
        """初始化Agent服务"""
        self.llm = ChatOpenAI(
            # api_key=os.getenv("OPENAI_API_KEY"),
            # model_name="gpt-3.5-turbo",
            model="qwen-max",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url=os.getenv("API_BASE_URL"),
            temperature=0.3
        )
        self.str_output_parser = StrOutputParser()
        self.json_output_parser = JsonOutputParser()
        # 存储请假记录
        self.leave_records: Dict[str, List[Dict[str, Any]]] = {}
        # 存储会议记录
        self.meeting_records: Dict[str, List[Dict[str, Any]]] = {}
    
    async def process_leave_request(self, space_id: str, request_text: str) -> Dict[str, Any]:
        """
        处理请假请求
        
        Args:
            space_id: 空间ID
            request_text: 请假请求文本
            
        Returns:
            处理结果
        """
        # 创建解析请假信息的提示模板
        parse_prompt = ChatPromptTemplate.from_template("""
        请从用户的请假请求中提取以下信息并格式化为JSON：
        - 员工姓名
        - 请假类型（如：年假、病假、事假等）
        - 开始日期（格式：YYYY-MM-DD）
        - 结束日期（格式：YYYY-MM-DD）
        - 请假原因
        - 请假天数（计算从开始日期到结束日期的天数）
        
        用户的请假请求：
        {request_text}
        
        请严格按照JSON格式输出，不要包含任何其他内容。
        """)
        
        # 创建解析链
        parse_chain = parse_prompt | self.llm | self.str_output_parser
        
        try:
            # 解析请假信息
            leave_info_str = await parse_chain.ainvoke({"request_text": request_text})
            
            # 解析JSON字符串
            import json
            leave_info = json.loads(leave_info_str)
            
            # 验证日期
            start_date = datetime.strptime(leave_info["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(leave_info["end_date"], "%Y-%m-%d")
            
            if start_date > end_date:
                return {
                    "status": RESPONSE_STATUS_FAILED,
                    "message": "开始日期不能晚于结束日期"
                }
            
            # 计算请假天数
            leave_info["duration_days"] = (end_date - start_date).days + 1
            
            # 保存请假记录
            if space_id not in self.leave_records:
                self.leave_records[space_id] = []
            self.leave_records[space_id].append({
                **leave_info,
                "request_time": datetime.now().isoformat(),
                "status": "pending"
            })
            
            # 生成确认回复
            confirm_prompt = ChatPromptTemplate.from_template("""
            请为用户生成一个请假申请确认回复。
            
            请假信息：
            员工姓名：{employee_name}
            请假类型：{leave_type}
            开始日期：{start_date}
            结束日期：{end_date}
            请假天数：{duration_days}天
            请假原因：{reason}
            
            请以友好、专业的语气确认请假申请已收到，并告知后续流程。
            """)
            
            confirm_chain = confirm_prompt | self.llm | self.str_output_parser
            confirmation = await confirm_chain.ainvoke(leave_info)
            
            return {
                "status": RESPONSE_STATUS_SUCCESS,
                "confirmation": confirmation,
                "leave_info": leave_info
            }
            
        except json.JSONDecodeError:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "无法解析请假请求，请提供更详细的信息"
            }
        except ValueError as e:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"日期格式错误: {str(e)}"
            }
        except Exception as e:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"处理请假请求失败: {str(e)}"
            }
    
    async def process_meeting_request(self, space_id: str, request_text: str) -> Dict[str, Any]:
        """
        处理会议预约请求
        
        Args:
            space_id: 空间ID
            request_text: 会议预约请求文本
            
        Returns:
            处理结果
        """
        # 创建解析会议信息的提示模板
        parse_prompt = ChatPromptTemplate.from_template("""
        请从用户的会议预约请求中提取以下信息并格式化为JSON：
        - 会议标题
        - 参会人员列表（格式为数组）
        - 会议时间（格式：YYYY-MM-DD HH:MM）
        - 会议时长（分钟）
        - 会议地点
        - 会议议程
        
        用户的会议预约请求：
        {request_text}
        
        请严格按照JSON格式输出，不要包含任何其他内容。
        """)
        
        # 创建解析链
        parse_chain = parse_prompt | self.llm | self.str_output_parser
        
        try:
            # 解析会议信息
            meeting_info_str = await parse_chain.ainvoke({"request_text": request_text})
            
            # 解析JSON字符串
            import json
            meeting_info = json.loads(meeting_info_str)
            
            # 验证会议时间
            meeting_datetime = datetime.strptime(meeting_info["meeting_time"], "%Y-%m-%d %H:%M")
            
            if meeting_datetime <= datetime.now():
                return {
                    "status": RESPONSE_STATUS_FAILED,
                    "message": "会议时间不能早于当前时间"
                }
            
            # 保存会议记录
            if space_id not in self.meeting_records:
                self.meeting_records[space_id] = []
            self.meeting_records[space_id].append({
                **meeting_info,
                "request_time": datetime.now().isoformat(),
                "status": "scheduled"
            })
            
            # 生成确认回复
            confirm_prompt = ChatPromptTemplate.from_template("""
            请为用户生成一个会议预约确认回复。
            
            会议信息：
            会议标题：{meeting_title}
            参会人员：{participants}
            会议时间：{meeting_time}
            会议时长：{duration_minutes}分钟
            会议地点：{location}
            会议议程：{agenda}
            
            请以友好、专业的语气确认会议已安排，并提供简要的会议提醒。
            """)
            
            # 格式化参会人员列表
            meeting_info["participants"] = ", ".join(meeting_info["participants"])
            
            confirm_chain = confirm_prompt | self.llm | self.str_output_parser
            confirmation = await confirm_chain.ainvoke(meeting_info)
            
            return {
                "status": RESPONSE_STATUS_SUCCESS,
                "confirmation": confirmation,
                "meeting_info": meeting_info
            }
            
        except json.JSONDecodeError:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "无法解析会议预约请求，请提供更详细的信息"
            }
        except ValueError as e:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"日期时间格式错误: {str(e)}"
            }
        except Exception as e:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": f"处理会议预约请求失败: {str(e)}"
            }
    
    async def list_leave_records(self, space_id: str) -> List[Dict[str, Any]]:
        """
        列出用户的请假记录
        
        Args:
            space_id: 空间ID
            
        Returns:
            请假记录列表
        """
        return self.leave_records.get(space_id, [])
    
    async def list_meeting_records(self, space_id: str) -> List[Dict[str, Any]]:
        """
        列出用户的会议记录
        
        Args:
            space_id: 空间ID
            
        Returns:
            会议记录列表
        """
        return self.meeting_records.get(space_id, [])

# 创建全局Agent服务实例
agent_service = AgentService()