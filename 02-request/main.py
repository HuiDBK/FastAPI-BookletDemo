#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 请求参数案例 }
# @Date: 2023/11/06 11:15
from typing import Optional

import uvicorn
from fastapi import FastAPI, Header, UploadFile, Path, Query, Depends, Request
from pydantic import BaseModel, Field

app = FastAPI(summary="请求参数案例")


@app.get("/query_params", summary="查询字符串参数Demo")
def with_query_params(name: str, age: int):
    return {"name": name, "age": age}


@app.get("/user/{user_id}/path_params", summary="路径参数Demo")
def with_path_params(user_id: int):
    return {"user_id": user_id}


class UserLoginIn(BaseModel):
    account: str = Field(..., description="账号")
    password: str = Field(..., description="密码")


@app.post("/user/login/json_params", summary="json参数demo")
def with_json_params(req_model: UserLoginIn):
    return req_model.model_dump()


@app.get("/user/detail/header_params", summary="请求头参数demo")
def with_header_params(
        token: str = Header(description="访问token"),
        user_agent: str = Header(description="用户代理"),
):
    return {"token": token, "User-Agent": user_agent}


@app.post("/file_upload/file_params", summary="文件参数demo")
async def with_file_params(file: UploadFile):
    return {"filename": file.filename, "file_size": file.size}


@app.get("/users/{user_id}/path_query_params", summary="路径参数+查询字符串参数demo")
def with_path_query_params(
        user_id: int = Path(description="用户ID"),
        age: int = Query(default=None, description="年龄查询")
):
    # 业务逻辑处理
    # logic_func(user_id=user_id, age=age)
    return {"user_id": user_id, "age": age}


class UserQueryIn(BaseModel):
    user_id: int = Field(Path(gt=0, description="用户ID"))
    name: Optional[str] = Field(Query(default=None, min_length=1, description="姓名"))
    age: Optional[int] = Field(Query(default=None, gt=0, description="年龄"))


@app.get("/users/{user_id}/path_query_params2", summary="路径参数+查询字符串参数BaseModel的demo")
def with_path_query_params(req_model: UserQueryIn = Depends(UserQueryIn)):
    # 业务逻辑处理
    # logic_func(req_model)
    return req_model.model_dump()


@app.get("/request_obj", summary="请求对象的demo")
def req_obj_demo(req: Request):
    print("req client ip", req.client.host)
    print("req method", req.method)
    print("req base_url", req.base_url)
    print("req url", req.url)

    print("Request", req)
    return {
        "client_ip": req.client.host,
        "method": req.method,
        "base_url": req.base_url,
        "url": req.url,
    }


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
