import os
import json
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
import logging

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RelativeDBService:
    """关系数据库服务类，处理MySQL数据库操作"""
    
    def __init__(self):
        """初始化数据库服务"""
        self.connection = None
        self.cursor = None
        self._connect_db()
        self._create_tables()
    
    def _connect_db(self):
        """连接到MySQL数据库"""
        try:
            # 从环境变量获取数据库配置
            db_config = {
                'host': os.getenv('DB_HOST', 'localhost'),
                'user': os.getenv('DB_USER', 'root'),
                'password': os.getenv('DB_PASSWORD', ''),
                'database': os.getenv('DB_NAME', 'ai_customer_service')
            }
            
            # 建立数据库连接
            self.connection = mysql.connector.connect(**db_config)
            
            if self.connection.is_connected():
                logger.info("成功连接到MySQL数据库")
                self.cursor = self.connection.cursor(dictionary=True)
                
        except Error as e:
            logger.error(f"数据库连接失败: {str(e)}")
            # 连接失败时不抛出异常，允许服务继续运行
    
    def _create_tables(self):
        """创建必要的数据表"""
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return
        
        try:
            # 创建用户表
            create_users_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                nickname VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_users_table_query)
            
            # 创建documents表
            create_documents_table_query = """
            CREATE TABLE IF NOT EXISTS documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                file_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(512) NOT NULL,
                file_size INT NOT NULL,
                document_ids TEXT NOT NULL,
                chunks_count INT NOT NULL,
                upload_time DATETIME NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_user_file (user_id, file_name),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
            
            self.cursor.execute(create_documents_table_query)
            self.connection.commit()
            logger.info("数据表创建成功")
            
        except Error as e:
            logger.error(f"创建数据表失败: {str(e)}")
    
    def save_document_info(self, user_id: str, document_info: Dict[str, Any]) -> bool:
        """
        保存文档信息到数据库
        
        Args:
            user_id: 用户ID
            document_info: 文档信息字典
            
        Returns:
            是否保存成功
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return False
        
        try:
            # 将document_ids列表转换为JSON字符串
            document_ids_json = json.dumps(document_info['document_ids'])
            
            # 使用INSERT ON DUPLICATE KEY UPDATE处理重复键
            query = """
            INSERT INTO documents 
            (user_id, file_name, file_path, file_size, document_ids, chunks_count, upload_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            file_path = VALUES(file_path),
            file_size = VALUES(file_size),
            document_ids = VALUES(document_ids),
            chunks_count = VALUES(chunks_count),
            upload_time = VALUES(upload_time)
            """
            
            values = (
                user_id,
                document_info['file_name'],
                document_info['file_path'],
                document_info['file_size'],
                document_ids_json,
                document_info['chunks_count'],
                document_info['upload_time']
            )
            
            self.cursor.execute(query, values)
            self.connection.commit()
            logger.info(f"文档信息保存成功: {user_id} - {document_info['file_name']}")
            return True
            
        except Error as e:
            logger.error(f"保存文档信息失败: {str(e)}")
            if self.connection.is_connected():
                self.connection.rollback()
            return False
    
    def get_document_info(self, user_id: str, file_name: str) -> Optional[Dict[str, Any]]:
        """
        获取文档信息
        
        Args:
            user_id: 用户ID
            file_name: 文件名
            
        Returns:
            文档信息字典，如果不存在则返回None
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return None
        
        try:
            query = """
            SELECT id, user_id, file_name, file_path, file_size, document_ids, 
                   chunks_count, upload_time, created_at
            FROM documents 
            WHERE user_id = %s AND file_name = %s
            """
            
            self.cursor.execute(query, (user_id, file_name))
            result = self.cursor.fetchone()
            
            if result:
                # 将JSON字符串转换回document_ids列表
                result['document_ids'] = json.loads(result['document_ids'])
                # 删除数据库特定字段
                result.pop('id', None)
                result.pop('created_at', None)
                return result
            
            return None
            
        except Error as e:
            logger.error(f"获取文档信息失败: {str(e)}")
            return None
    
    def create_user(self, account: str, password: str, nickname: str) -> Optional[int]:
        """
        创建新用户
        
        Args:
            account: 用户账号
            password: 加密后的密码
            nickname: 用户昵称
            
        Returns:
            新用户ID，失败则返回None
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return None
        
        try:
            query = "INSERT INTO users (account, password, nickname) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (account, password, nickname))
            self.connection.commit()
            return self.cursor.lastrowid
        except Error as e:
            logger.error(f"创建用户失败: {str(e)}")
            if self.connection.is_connected():
                self.connection.rollback()
            return None
    
    def get_user_by_account(self, account: str) -> Optional[Dict[str, Any]]:
        """
        通过账号获取用户信息
        
        Args:
            account: 用户账号
            
        Returns:
            用户信息字典，不存在则返回None
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return None
        
        try:
            query = "SELECT id, account, nickname, created_at FROM users WHERE account = %s"
            self.cursor.execute(query, (account,))
            return self.cursor.fetchone()
        except Error as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        通过ID获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户信息字典，不存在则返回None
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return None
        
        try:
            query = "SELECT id, account, nickname, created_at FROM users WHERE id = %s"
            self.cursor.execute(query, (user_id,))
            return self.cursor.fetchone()
        except Error as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            return None
    
    def delete_document_info(self, user_id: str, file_name: str) -> bool:
        """
        删除文档信息
        
        Args:
            user_id: 用户ID
            file_name: 文件名
            
        Returns:
            是否删除成功
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return False
        
        try:
            query = "DELETE FROM documents WHERE user_id = %s AND file_name = %s"
            self.cursor.execute(query, (user_id, file_name))
            self.connection.commit()
            
            logger.info(f"文档信息删除成功: {user_id} - {file_name}")
            return self.cursor.rowcount > 0
            
        except Error as e:
            logger.error(f"删除文档信息失败: {str(e)}")
            if self.connection.is_connected():
                self.connection.rollback()
            return False
    
    def list_space_documents(self, user_id: str) -> List[Dict[str, Any]]:
        """
        获取用户的所有文档信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            文档信息列表
        """
        if not self.connection or not self.connection.is_connected():
            self._connect_db()
            
        if not self.connection or not self.connection.is_connected():
            return []
        
        try:
            query = """
            SELECT id, user_id, file_name, file_path, file_size, document_ids, 
                   chunks_count, upload_time, created_at
            FROM documents 
            WHERE user_id = %s
            ORDER BY upload_time DESC
            """
            
            self.cursor.execute(query, (user_id,))
            results = self.cursor.fetchall()
            
            # 处理结果
            documents = []
            for result in results:
                # 将JSON字符串转换回document_ids列表
                result['document_ids'] = json.loads(result['document_ids'])
                # 删除数据库特定字段
                result.pop('id', None)
                result.pop('created_at', None)
                documents.append(result)
            
            return documents
            
        except Error as e:
            logger.error(f"获取用户文档列表失败: {str(e)}")
            return []
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("数据库连接已关闭")

# 创建全局数据库服务实例
relative_db_service = RelativeDBService()