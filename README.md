# AI超级智能客服

基于LangChain和LangGraph的智能客服系统，支持RAG功能和Agent功能等。
[在线体验](http://115.190.242.191/)

## 功能展示

#### 带有记忆的聊天
![项目](resources/project01.gif)
#### 知识库有内容的RAG展示
![聊天](resources/project02.gif)
#### 日程会议的创建和查询（Agent其他所有功能均支持此项操作）
![项目](resources/project03.gif)
#### 日程会议列表修改指定记录属性（Agent其他所有功能均支持此项操作）
![项目](resources/project05.gif)
#### 日程会议列表删除指定记录（Agent其他所有功能均支持此项操作）
![项目](resources/project06.gif)
#### 我的昵称的修改
![项目](resources/project04.gif)


### RAG功能
- 支持用户注册登录
- 支持用户上传PDF、DOCX、XLSX、TXT、MD、CSV格式的文档
- 支持向量存储和检索，基于用户上传的文档进行问答
- 支持删除已上传的文档

### Agent功能
- 智能日程会议：便捷创建、查询和管理您的日程会议，高效规划团队协作时间
- 智能请假申请：轻松提交请假申请并查询审批状态，简化人事管理流程
- 预定机票：智能搜索并预订国内外航班，支持行程管理和退改签操作
- 预定酒店：一键预订全球酒店，享受会员优惠价，灵活管理入住信息
- 修改昵称：个性化您的账户昵称，展现独特身份标识

## 技术栈

- **后端框架**：FastAPI
- **大语言模型集成**：LangChain, LangGraph
- **Embeddings**：text-embedding-v3
- **向量数据库**：ChromaDB
- **关系数据库**：Mysql
- **文档处理**：PDF, Text, Excel, Markdown
- **API服务**：Qwen API
- **Web框架**：Svelte
- **Web组件库**：Svelte Material UI

## 快速开始

### 环境要求

- Python 3.9.13+
- pip

### 安装步骤

1. Clone项目
   ```bash
   git clone https://github.com/deep-fish-pixel/ai_customer_service.git
   ```

2. 安装依赖
   ```bash
   pip3 install -r requirements.txt
   ```

3. 配置环境变量
   - 复制 `.env` 文件中的示例配置
   - 设置本机环境变量 `DASHSCOPE_API_KEY` 为您的实际API密钥
   - 设置本机环境变量 `API_BASE_URL` 为您的Model服务地址
   - 设置本机环境变量 `LANGCHAIN_API_KEY` 为您的LangChain密钥
   - 设置本机环境变量 `DB_HOST` 为您的Mysql ip
   - 设置本机环境变量 `DB_USER` 为您的Mysql user
   - 设置本机环境变量 `DB_PASSWORD` 为您的Mysql password
   - 设置本机环境变量 `DB_NAME` 为您的Mysql dbname

4. 运行应用
   ```bash
   python3 main.py
   ```

5. 访问API文档
   - 打开浏览器访问：http://localhost:8000/docs

## API接口说明

### 用户注册接口
- `POST /api/user/register` - 注册账号
- `POST /api/user/login` - 登录账号
- `POST /api/user/info` - 获取用户信息

### 聊天接口
- `POST /api/chat/send` - 发送消息给客服

### 文档管理接口
- `POST /api/documents/upload` - 上传文档
- `DELETE /api/documents/{file_name}` - 删除文档
- `GET /api/documents/` - 列出所有文档

### 多模态接口
- `POST /api/model/image_tasks/{task_id}` - 查询图片任务信息


## 项目结构

```
├── main.py                 # 应用入口
├── requirements.txt        # 依赖列表
├── .env                    # 环境变量配置
├── src/                    # 源代码目录
│   ├── api/                # API接口
│   │   └── endpoints/      # 具体的端点实现
│   ├── enums/              # action内容状态
│   ├── services/           # 业务逻辑层
│   ├── utils/              # 工具类
│   └── models/             # 数据模型
├── uploads/                # 文件上传目录
├── chromadb/               # 向量数据库目录
└── front/                  # 前端项目
```

## [前端项目](./front/README.md) 
