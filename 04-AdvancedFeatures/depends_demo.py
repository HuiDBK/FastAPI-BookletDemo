#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: depends_demo.py
# @Desc: { 模块描述 }
# @Date: 2024/05/21 11:05
import asyncio
import time
from contextvars import ContextVar

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Path, Request, BackgroundTasks
from typing import Union, Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

REQ_CTX: ContextVar[Union[Request, None]] = ContextVar("req_ctx", default=None)
BG_TASK_EXECUTOR: ContextVar[Union[BackgroundTasks, None]] = ContextVar("bg_task_executor", default=None)


async def set_req_and_bg_tasks(req: Request, bg_tasks: BackgroundTasks):
    """全局依赖把请求对象与后台任务处理器存储到上下文变量中"""
    REQ_CTX.set(req)
    BG_TASK_EXECUTOR.set(bg_tasks)


app = FastAPI(description="depends 使用", dependencies=[Depends(set_req_and_bg_tasks)])


async def req_bg_tasks_logic(name: str, sleep_seconds: int = 5):
    req = REQ_CTX.get()
    print(req.url)

    ret = f"name {name} sleep {sleep_seconds}s"

    def bg_task_demo():
        time.sleep(sleep_seconds)
        print("bg_task_demo", ret)

    # 模拟添加后台任务
    bg_task_executor = BG_TASK_EXECUTOR.get()
    bg_task_executor.add_task(bg_task_demo)
    return ret


@app.get("/req_bg_tasks_demo")
async def req_bg_tasks_demo(name: str, sleep_seconds: int = 5):
    ret = await req_bg_tasks_logic(name, sleep_seconds)
    return ret


@app.get("/bg_tasks_demo")
async def bg_task_demo(bg_tasks: BackgroundTasks):
    def sync_bg_task_test(name, sleep_seconds: int = 3):
        print("sync_bg_task_test running")
        time.sleep(sleep_seconds)
        print(f"sync_bg_task_test {name} sleep {sleep_seconds}s end")

    async def async_bg_task_test(name, sleep_seconds: int = 3):
        print("async_bg_task_test running")
        await asyncio.sleep(sleep_seconds)
        print(f"async_bg_task_test {name} sleep {sleep_seconds}s end")

    # 分别添加同步、异步io的后台任务
    bg_tasks.add_task(sync_bg_task_test, name="hui-sync", sleep_seconds=1)
    bg_tasks.add_task(async_bg_task_test, name="hui-async", sleep_seconds=2)

    return "bg_task_demo"


class PageModel(BaseModel):
    offset: int = Field(0, description="偏移量")
    limit: int = Field(10, description="每页大小")


def page_parameters(
        curr_page: int = 1, page_size: int = 10
):
    offset = (curr_page - 1) * page_size
    if offset < 0 or page_size > 1000:
        raise HTTPException(status_code=400, detail="Limit must be less than 100")

    return PageModel(offset=offset, limit=page_size)


@app.get("/v1/items/")
async def read_items(curr_page: int = Query(1), page_size: int = Query(10)):
    page_model = page_parameters(curr_page, page_size)
    items = ["item1", "item2", "item3"][page_model.offset:page_model.offset + page_model.limit]
    return {"items": items}


@app.get("/v1/users/")
async def read_users(curr_page: int = Query(1), page_size: int = Query(10)):
    page_model = page_parameters(curr_page, page_size)
    users = ["user1", "user2", "user3"][page_model.offset:page_model.offset + page_model.limit]
    return users


@app.get("/v2/items/")
async def read_items(page_model: PageModel = Depends(page_parameters)):
    items = ["item1", "item2", "item3"][page_model.offset:page_model.offset + page_model.limit]
    return {"items": items}


@app.get("/v2/users/")
async def read_users(page_model: PageModel = Depends(page_parameters)):
    users = ["user1", "user2", "user3"][page_model.offset:page_model.offset + page_model.limit]
    return users


class UserQueryIn(BaseModel):
    user_id: int = Path(description="用户ID")
    name: Optional[str] = Query(default=None, description="姓名")
    age: Optional[int] = Query(default=None, description="年龄")


@app.get("/users/{user_id}/path_query_params", summary="路径参数+查询字符串参数BaseModel的demo")
def with_path_query_params(req_model: UserQueryIn = Depends(UserQueryIn)):
    # 业务逻辑处理
    # logic_func(req_model)
    return req_model.model_dump()


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
