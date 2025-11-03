from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging

from src import RESPONSE_STATUS_SUCCESS, RESPONSE_STATUS_FAILED
from src.services.relative_db_service import RelativeDBService
from src.services.auth_service import AuthService

# 创建路由
router = APIRouter()

# 配置日志
logger = logging.getLogger(__name__)

# 初始化服务
db_service = RelativeDBService()
auth_service = AuthService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

# Pydantic模型
class UserRegisterRequest(BaseModel):
    account: str
    password: str
    nickname: str

class UserLoginRequest(BaseModel):
    account: str
    password: str

# 依赖项：获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    user_id = auth_service.extract_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@router.post("/register", response_model=Dict[str, Any])
async def register_user(request: UserRegisterRequest) -> Dict[str, Any]:
    """用户注册接口"""
    try:
        # 检查用户是否已存在
        existing_user = db_service.get_user_by_account(request.account)
        if existing_user:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "账号已存在",
                "data": None
            }
        
        # 密码加密
        hashed_password = auth_service.hash_password(request.password)
        
        # 创建用户
        user_id = db_service.create_user(
            account=request.account,
            password=hashed_password,
            nickname=request.nickname
        )
        
        if not user_id:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "用户创建失败",
                "data": None
            }
        
        return {
            "status": RESPONSE_STATUS_SUCCESS,
            "message": "用户注册成功",
            "data": {"user_id": user_id, "account": request.account, "nickname": request.nickname}
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"注册失败: {str(e)}")
        return {
            "status": RESPONSE_STATUS_FAILED,
            "message": f"注册失败: {str(e)}",
            "data": None
        }

@router.post("/login", response_model=Dict[str, Any])
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, Any]:
    """用户登录接口，返回JWT令牌"""
    try:
        # 获取用户
        user = db_service.get_user_by_account(form_data.username)
        if not user:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "账号或密码错误",
                "data": None
            }
        
        # 验证密码
        if not auth_service.verify_password(form_data.password, user["password"]):
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "账号或密码错误",
                "data": None
            }
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=30)
        access_token = auth_service.create_access_token(
            data={"sub": user["id"]},
            expires_delta=access_token_expires
        )
        
        return {
            "status": RESPONSE_STATUS_SUCCESS,
            "message": "登录成功",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user_id": user["id"],
                "account": user["account"],
                "nickname": user["nickname"]
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return {
            "status": RESPONSE_STATUS_FAILED,
            "message": f"登录失败: {str(e)}",
            "data": None
        }

@router.get("/info", response_model=Dict[str, Any])
async def get_user_info(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """获取当前用户信息接口"""
    try:
        return {
            "status": RESPONSE_STATUS_SUCCESS,
            "message": "获取用户信息成功",
            "data": current_user
        }
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return {
            "status": RESPONSE_STATUS_FAILED,
            "message": f"获取用户信息失败: {str(e)}",
            "data": None
        }

# 补充缺失的导入
from datetime import timedelta