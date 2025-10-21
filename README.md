# 小智智能客服系统

基于LangChain和LangGraph的智能客服系统，支持RAG功能和Agent功能。

## 功能特性

### RAG功能
- 支持用户上传PDF、TXT、MD、CSV格式的文档
- 支持向量存储和检索，基于用户上传的文档进行问答
- 支持删除已上传的文档

### Agent功能
- 智能请假申请：自动识别请假信息，生成请假记录
- 智能会议预约：自动识别会议信息，生成会议记录

## 技术栈

- **后端框架**：FastAPI
- **大语言模型集成**：LangChain, LangGraph
- **向量数据库**：ChromaDB
- **文档处理**：PyPDF, BeautifulSoup, Markdown
- **API服务**：OpenAI API

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. 克隆项目（如果适用）

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置环境变量
   - 复制 `.env` 文件中的示例配置
   - 替换 `OPENAI_API_KEY` 为您的实际API密钥

4. 运行应用
   ```bash
   python main.py
   ```

5. 访问API文档
   - 打开浏览器访问：http://localhost:8000/docs

## API接口说明

### 聊天接口
- `POST /api/chat/send` - 发送消息给客服

### 文档管理接口
- `POST /api/documents/upload` - 上传文档
- `DELETE /api/documents/{file_name}` - 删除文档
- `GET /api/documents/` - 列出所有文档

### Agent功能接口
- `POST /api/agent/leave` - 申请请假
- `POST /api/agent/meeting` - 预约会议
- `GET /api/agent/leave/records` - 获取请假记录
- `GET /api/agent/meeting/records` - 获取会议记录

## 使用示例

### 上传文档
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "X-User-Id: user123" \
  -F "file=@example.pdf"
```

### 发送消息
```bash
curl -X POST "http://localhost:8000/api/chat/send" \
  -H "X-User-Id: user123" \
  -H "Content-Type: application/json" \
  -d '{"query": "请告诉我关于公司政策的信息", "use_rag": true}'
```

### 申请请假
```bash
curl -X POST "http://localhost:8000/api/agent/leave" \
  -H "X-User-Id: user123" \
  -H "Content-Type: application/json" \
  -d '{"request_text": "我需要请年假，从2024年6月1日到6月3日，共3天，因为家里有事。"}'
```

## 注意事项

1. 请确保您已正确配置OpenAI API密钥
2. 上传的文档会被处理并存储在向量数据库中
3. 目前系统使用内存存储记录，重启服务后记录会丢失
4. 在生产环境中，请配置合适的CORS策略和安全措施

## 项目结构

```
├── main.py                 # 应用入口
├── requirements.txt        # 依赖列表
├── .env                    # 环境变量配置
├── src/                    # 源代码目录
│   ├── api/                # API接口
│   │   └── endpoints/      # 具体的端点实现
│   ├── services/           # 业务逻辑层
│   ├── utils/              # 工具类
│   └── models/             # 数据模型
├── uploads/                # 文件上传目录
└── chromadb/               # 向量数据库目录
```