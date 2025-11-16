from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import os
import logging
from dotenv import load_dotenv
import bcrypt

# 配置日志
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 密码加密上下文
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
except Exception as e:
    logger.warning(f"CryptContext initialization warning: {str(e)}")
    # Fallback configuration to handle bcrypt version issues
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """加密密码"""
        try:
            # bcrypt has a 72-byte limit, so we truncate if necessary
            password_bytes = password.encode('utf-8')
            if len(password_bytes) > 72:
                # Truncate to exactly 72 bytes
                password_bytes = password_bytes[:72]
                logger.warning(f"Password truncated to 72 bytes for bcrypt compatibility")
            
            # Use bcrypt directly to avoid passlib issues
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_bytes, salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Password hashing failed: {str(e)}")
            raise ValueError(f"Password hashing failed: {str(e)}")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        try:
            # bcrypt has a 72-byte limit, so we truncate if necessary
            password_bytes = plain_password.encode('utf-8')
            if len(password_bytes) > 72:
                password_bytes = password_bytes[:72]
            
            # Use bcrypt directly to avoid passlib issues
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception as e:
            logger.error(f"Password verification failed: {str(e)}")
            return False

    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """创建JWT访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        payload = AuthService.extract_user_id_from_token(encoded_jwt)
        return encoded_jwt

    @staticmethod
    def extract_user_id_from_token(token: str) -> Optional[int]:
        """从令牌中提取用户ID"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except jwt.exceptions.PyJWTError as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"JWT解码失败: {str(e)}")
            return None