from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
# 导入并注册路由
from src.api.endpoints import chat, documents, agent

# 加载环境变量
load_dotenv()

# 创建FastAPI应用
app = FastAPI(
    title=os.getenv("APP_NAME", "小智智能客服"),
    description="基于LangChain和LangGraph的智能客服系统，支持RAG和Agent功能",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router, prefix="/api/chat", tags=["聊天"])
app.include_router(documents.router, prefix="/api/documents", tags=["文档管理"])
app.include_router(agent.router, prefix="/api/agent", tags=["Agent功能"])

# 根路径
@app.get("/")
async def root():
    return {"message": "欢迎使用小智智能客服系统！"}

# 健康检查
@app.get("/health")
async def health_check():
    print('======health_check')
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )