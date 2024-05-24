#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: def_async_def.py
# @Desc: { 模块描述 }
# @Date: 2024/05/21 11:06
import uvicorn
from fastapi import FastAPI
import requests
import httpx
import aiohttp

app = FastAPI(description="同步异步路由函数")

aio_client = httpx.AsyncClient()
aio_session: aiohttp.ClientSession = None
req_session = requests.Session()


@app.on_event("startup")
async def startup_event():
    global aio_session
    aio_session = aiohttp.ClientSession()


async def async_get(url):
    # async with aio_session.get(url) as resp:
    #     return resp

    resp = await aio_client.get(url)
    return resp


@app.get("/ping")
async def ping():
    return "pong"


@app.get("/async_route_func_demo")
async def async_route_func():
    url = "https://juejin.cn/"
    resp = await async_get(url)
    # print("resp", resp)
    return "async_route_func_demo"


@app.get("/async_route_use_sync_io_demo")
async def async_route_func():
    url = "https://juejin.cn/"
    resp = req_session.get(url)
    # print("resp", resp)
    return "async_route_func_demo"


@app.get("/sync_route_func_demo")
def sync_route_func():
    url = "https://juejin.cn/"
    resp = req_session.get(url)
    # print("resp", resp)
    return "sync_route_func_demo"


def main():
    uvicorn.run(app, log_level="warning")


if __name__ == '__main__':
    main()
