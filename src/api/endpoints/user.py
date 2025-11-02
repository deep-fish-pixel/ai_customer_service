from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
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
    space_id: Optional[str] = None
    space_name: Optional[str] = None
    space_description: Optional[str] = ""

class UserLoginRequest(BaseModel):
    account: str
    password: str

class SpaceCreateRequest(BaseModel):
    name: str
    description: Optional[str] = ""

class InviteUserRequest(BaseModel):
    space_id: str
    invite_account: str
    role: str = "member"

class UserResponse(BaseModel):
    id: int
    account: str
    nickname: str
    created_at: Optional[str] = None

class SpaceResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    role: str
    created_at: Optional[str] = None

class UserWithSpacesResponse(UserResponse):
    spaces: List[SpaceResponse] = []

# 依赖项
def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """获取当前登录用户ID"""
    user_id = auth_service.extract_user_id_from_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的身份验证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """获取当前登录用户信息"""
    user_id = get_current_user_id(token)
    user = db_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

# API接口
@router.post("/register", response_model=Dict[str, Any])
async def register_user(user_data: UserRegisterRequest):
    """用户注册接口，支持同时创建空间"""
    try:
        # 检查用户是否已存在
        existing_user = db_service.get_user_by_account(user_data.account)
        if existing_user:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "账号已存在",
                "data": None
            }

        # 哈希密码
        hashed_password = auth_service.hash_password(user_data.password)

        # 创建用户
        user_id = db_service.create_user(
            account=user_data.account,
            password=hashed_password,
            nickname=user_data.nickname
        )

        if user_id <= 0:
            return {
                "status": RESPONSE_STATUS_FAILED,
                "message": "用户创建失败",
                "data": None
            }

        # 如果提供了空间信息，创建空间并绑定用户
        if user_data.space_id and user_data.space_name:
            # 检查空间是否已存在
            # 注意：这里需要实现检查空间是否存在的方法
            # 简化处理：直接尝试创建空间
            success = db_service.create_space(
                space_id=user_data.space_id,
                name=user_data.space_name,
                description=user_data.space_description,
                user_id=user_id
            )
            if not success:
                # 如果空间创建失败，回滚用户创建
                # 注意：实际应用中需要更完善的事务处理
                return {
                    "status": RESPONSE_STATUS_FAILED,
                    "message": "用户创建成功，但空间创建失败",
                    "data": None
                }

        # 生成令牌
        token = auth_service.create_access_token(user_id)

        return {
            "status": RESPONSE_STATUS_SUCCESS,
            "message": "用户注册成功",
            "data": {
                "user_id": user_id,
                "token": token
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户注册失败: {str(e)}")
        return {
            "status": RESPONSE_STATUS_FAILED,
            "message": f"注册失败: {str(e)}",
            "data": None
        }

@router.post("/login", response_model=Dict[str, Any])
async def login_user(user_data: UserLoginRequest):
    """用户登录接口"""
    try:
        # 获取用户信息
        user = db_service.get_user_by_account(user_data.account)
        if not user:
            raise HTTPException(status_code=401, detail="账号或密码错误")

        # 验证密码
        if not auth_service.verify_password(user_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="账号或密码错误")

        # 获取用户空间列表
        spaces = db_service.get_user_spaces(user["id"])

        # 生成令牌
        token = auth_service.create_access_token(user["id"])

        return {
            "status": RESPONSE_STATUS_SUCCESS,
            "message": "登录成功",
            "data": {
                "user": user,
                "spaces": spaces,
                "token": token
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"用户登录失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

@router.get("/info", response_model=UserWithSpacesResponse)
async def get_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """获取当前用户信息及空间列表"""
    try:
        # 获取用户空间列表 Authorization: Bearer <your-jwt-token>
        spaces = db_service.get_user_spaces(current_user["id"])
        user_with_spaces = {**current_user, "spaces": spaces}
        return user_with_spaces
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取用户信息失败: {str(e)}")

@router.post("/spaces", response_model=Dict[str, Any])
async def create_space(
    space_data: SpaceCreateRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """创建新空间"""
    try:
        # 生成唯一空间ID
        space_id = str(uuid.uuid4())

        # 创建空间
        success = db_service.create_space(
            space_id=space_id,
            name=space_data.name,
            description=space_data.description,
            user_id=current_user["id"]
        )

        if not success:
            raise HTTPException(status_code=500, detail="空间创建失败")

        return {
            "status": RESPONSE_STATUS_SUCCESS,
            "message": "空间创建成功",
            "data": {
                "space_id": space_id,
                "name": space_data.name
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"创建空间失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建空间失败: {str(e)}")

@router.post("/spaces/invite", response_model=Dict[str, Any])
async def invite_user_to_space(
    invite_data: InviteUserRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """邀请用户加入空间"""
    try:
        # 检查当前用户是否在空间中且有权限邀请
        is_in_space = db_service.is_user_in_space(current_user["id"], invite_data.space_id)
        if not is_in_space:
            raise HTTPException(status_code=403, detail="您没有权限邀请用户加入此空间")

        # 检查被邀请用户是否存在
        invited_user = db_service.get_user_by_account(invite_data.invite_account)
        if not invited_user:
            raise HTTPException(status_code=404, detail="被邀请用户不存在")

        # 添加用户到空间
        success = db_service.add_user_to_space(
            user_id=invited_user["id"],
            space_id=invite_data.space_id,
            role=invite_data.role
        )

        if not success:
            raise HTTPException(status_code=500, detail="邀请用户失败")

        return {
            "status": RESPONSE_STATUS_SUCCESS,
            "message": f"邀请用户{invite_data.invite_account}成功",
            "data": {
                "space_id": invite_data.space_id,
                "invited_user_id": invited_user["id"],
                "role": invite_data.role
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"邀请用户失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"邀请用户失败: {str(e)}")