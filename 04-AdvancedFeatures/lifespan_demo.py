#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: lifespan_demo.py
# @Desc: { 模块描述 }
# @Date: 2024/06/25 17:43
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan_demo(app: FastAPI):
    # 应用启动
    await startup()
    yield
    # 应用关闭
    await shutdown()


app = FastAPI(lifespan=lifespan_demo)


async def init_setup():
    """初始化配置"""
    print("初始化日志、数据库...")


# @app.on_event("startup")
async def startup():
    """应用启动前处理"""
    await init_setup()


# @app.on_event("shutdown")
async def shutdown():
    """应用关闭时处理"""
    print("关闭数据库连接等...")
    print("Shutting down")


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
