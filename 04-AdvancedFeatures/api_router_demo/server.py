#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: api_router.py
# @Desc: { 模块描述 }
# @Date: 2024/06/28 11:35
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


# app = FastAPI(lifespan=lifespan, description="APIRouter模块路由Demo")
app = FastAPI(lifespan=lifespan, routes=api_router.routes, description="APIRouter模块路由Demo")


async def startup():
    # 初始化路由
    # app.include_router(api_router)

    # 初始化资源...
    pass


async def shutdown():
    print("释放资源")
    print("Shutting down...")


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
