#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: middleware_demo.py
# @Desc: { 模块描述 }
# @Date: 2024/05/21 11:07
import time
import uvicorn
from fastapi import FastAPI, Request
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class APIProcessTimeMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


# app = FastAPI(description="中间件demo")
app = FastAPI(description="中间件demo", middleware=[Middleware(APIProcessTimeMiddleware)])
# app.add_middleware(APIProcessTimeMiddleware)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response


@app.get("/middleware_demo")
async def middleware_demo():
    return {"demo": "middleware_demo"}


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
