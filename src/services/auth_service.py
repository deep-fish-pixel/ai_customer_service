import os
import jwt
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# JWT配置
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')  # 生产环境应使用环境变量
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 令牌过期时间

class AuthService:
    """认证服务类，处理密码哈希和JWT令牌"""
    
    def hash_password(self, password: str) -> str:
        """
        使用SHA-256哈希密码
        
        Args:
            password: 原始密码
            
        Returns:
            哈希后的密码
        """
        # 在生产环境中应使用更安全的哈希算法如bcrypt
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            plain_password: 原始密码
            hashed_password: 哈希后的密码
            
        Returns:
            密码是否匹配
        """
        return self.hash_password(plain_password) == hashed_password
    
    def create_access_token(self, user_id: int) -> str:
        """
        创建JWT访问令牌
        
        Args:
            user_id: 用户ID
            
        Returns:
            JWT令牌
        """
        # 设置过期时间
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # 创建令牌数据
        to_encode = {
            "sub": str(user_id),
            "exp": expire
        }
        
        # 编码令牌
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def extract_user_id_from_token(self, token: str) -> Optional[int]:
        """
        从令牌中提取用户ID
        
        Args:
            token: JWT令牌
            
        Returns:
            用户ID，失败返回None
        """
        try:
            # 解码令牌
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # 提取用户ID
            user_id_str: str = payload.get("sub")
            if user_id_str is None:
                return None
            
            return int(user_id_str)
        except jwt.PyJWTError:
            logger.error("令牌验证失败")
            return None
        except ValueError:
            logger.error("用户ID格式错误")
            return None