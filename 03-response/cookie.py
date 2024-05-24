#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 注册登陆demo }
# @Date: 2023/08/07 16:08
from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI, Body, Cookie, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(description="注册登陆demo")
app.add_middleware(
    SessionMiddleware,
    session_cookie="user_id",
    secret_key="random-secret-key",
    max_age=int(timedelta(days=1).total_seconds())
)


@app.post("/set_cookie")
def set_cookie_demo(user_id: int = Body(description="用户ID")):
    resp = JSONResponse(content={"user_id": user_id, "demo": "set_cookie"})
    max_age = int(timedelta(hours=6).total_seconds())  # cookie 有效期
    resp.set_cookie(key="user_id", value=str(user_id), max_age=max_age)
    return resp


@app.get("/get_cookie")
def get_cookie_demo(user_id: int = Cookie(default=0)):
    print("user_id", user_id)
    resp = JSONResponse(content={"user_id": user_id, "demo": "get_cookie"})
    return resp


user_infos = [
    {"id": 1, "username": "hui", "password": "123456"},
    {"id": 2, "username": "quan", "password": "123456"},
]

# key user_id value user info and expire_time
user_session = {
    # 1: {"user": {"id": 1, "username": "hui"}, "expire_time": datetime.now() + timedelta(hours=2)}
}


@app.get(path="/index")
def index():
    return "index"


@app.get(path="/users/detail")
def user_detail(request: Request, user_id: str = Cookie(default=0)):
    # 登陆认证
    user_id = request.session.get("user_id")
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

    return JSONResponse(content=user_info.get("user"))


def get_user(username, password):
    print("user_infos", user_infos)
    for user in user_infos:
        if user.get("username") == username and user.get("password") == password:
            return {"id": user.get("id"), "username": user.get("username")}


class LoginModel(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="用户名")
    password: str = Field(min_length=6, description="密码")


@app.post(path="/users/register")
def register(user: LoginModel):
    print("user", user)
    max_id = max([user.get("id") for user in user_infos]) or 0
    user_id = max_id + 1
    register_user = {"id": user_id, **user.model_dump()}
    user_infos.append(register_user)
    print("user_infos", user_infos)
    return JSONResponse(content={"user_id": user_id, "message": "ok"})


@app.post(path="/users/login")
def login(
        request: Request, user: LoginModel
):
    user = get_user(user.username, user.password)
    print("user", user)

    if not user:
        return JSONResponse(content={"code": -1, "message": "用户or密码错误", "data": {}})

    # 登陆成功设置cookie
    resp = JSONResponse(content={"code": 0, "message": "ok", "data": {}})
    # resp.set_cookie(key="user_id", value=user.get("id"), max_age=int(timedelta(days=1).total_seconds()))
    request.session["user_id"] = user.get("id")

    # 保存用户session
    user_session[user.get("id")] = {"user": user, "expire_time": datetime.now() + timedelta(days=1)}

    return resp


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
