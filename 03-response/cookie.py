#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 模块描述 }
# @Date: 2023/08/07 16:08
from datetime import datetime, timedelta
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Body, Cookie
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(description="hello world")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_infos = [
    {"id": 1, "username": "hui", "password": "123456"},
    {"id": 2, "username": "quan", "password": "123456"},
]

# key user_id value user info and expire_time
user_session = {
    # 1: {"user": {"id": 1, "username": "hui"}, "expire_time": datetime.now() + timedelta(days=1)}
}


@app.get(path="/")
def index():
    return "index"


@app.get(path="/hello")
def hello(user_id: Annotated[int, Cookie()] = None):
    # 登陆认证
    print("user_id", user_id)

    user_info = user_session.get(user_id)
    if not user_info:
        return JSONResponse(
            content={"code": -1, "message": "未登陆", "data": {}}
        )

    user = user_info.get("user")
    expire_time = user_info.get("expire_time")
    print("user", user)

    if datetime.now() > expire_time:
        return JSONResponse(
            status_code=401,
            content={"code": -1, "message": "登陆过期，请重新登陆", "data": {}}
        )

    return JSONResponse(
        content={"code": 0, "message": "hello world", "data": {}}
    )


def get_user(username, password):
    for user in user_infos:
        if user.get("username") == username and user.get("password") == password:
            return user


@app.post(path="/login")
def login(
        username: str = Body(min_length=3, max_length=20, description="用户名"),
        password: str = Body(min_length=6, description="密码"),
):
    user = get_user(username, password)

    if not user:
        return JSONResponse(content={"code": -1, "message": "用户or密码错误", "data": {}})

    # 登陆成功设置cookie
    resp = JSONResponse(content={"code": 0, "message": "OK", "data": {}})
    resp.set_cookie(key="user_id", value=user.get("id"), max_age=int(timedelta(days=1).total_seconds()))

    # 保存用户session
    user_session[user.get("id")] = {"user": user, "expire_time": datetime.now() + timedelta(days=1)}

    return resp


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
