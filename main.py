# web 服务器
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os

from app import logger,app_config

#from wordease.api.user import api_user

logo_tmpl=r"""
----------------------------------------
            app已经运行
----------------------------------------
"""

def check_env():
    os.makedirs("data/", exist_ok=True)


app = FastAPI(
    title="API",
    description="API模板",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)
@app.get("/")
async def root():
    return {"message": "欢迎使用API模板"}
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],  # 允许所有头
    )

if __name__ == '__main__':
    #app.include_router(api_user, prefix="/user", tags=["用户接口"])
    check_env()
    mysql_config = app_config.mysql_config
    # 初始化 Tortoise ORM
    register_tortoise(
        app,
        config=mysql_config,
        generate_schemas=False,  # 开发环境可以生成表结构，生产环境建议关闭
        add_exception_handlers=True,  # 显示错误信息
    )

    
    logger.info(logo_tmpl)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    