#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { 响应处理 }
# @Date: 2023/12/05 15:20
from typing import Optional

import uvicorn
from fastapi import FastAPI, Response
from pydantic import BaseModel, Field
from fastapi.responses import (
    HTMLResponse, JSONResponse, UJSONResponse, ORJSONResponse,
    StreamingResponse, FileResponse, RedirectResponse
)

app = FastAPI(summary="响应处理")


@app.get("/plain_text_demo")
async def plain_text_demo():
    # 默认响应头的 content-type 是 application/json
    return "hello fastapi"


@app.get("/plain_text_demo2")
async def plain_text_demo():
    return Response(content="hello fastapi 2", media_type="text/plain")


@app.get("/html_demo")
async def html_demo():
    html_text = "<h1> hello fastapi </>"
    # return Response(content=html_text, media_type="text/html")

    return HTMLResponse(content=html_text)


@app.get("/json_demo1")
async def json_demo():
    return {"name": "hui", "age": 18}


@app.get("/json_demo2")
async def json_demo2():
    json_content = {
        "code": 0,
        "message": "ok",
        "data": {"name": "hui", "age": 22}
    }
    return JSONResponse(content=json_content)


@app.get("/ujson_demo")
async def ujson_demo():
    ujson_content = {
        "code": 0,
        "message": "ok",
        "data": {"json_type": "ujson"}
    }
    return UJSONResponse(content=ujson_content)


@app.get("/orjson_demo")
async def orjson_demo():
    orjson_content = {
        "code": 0,
        "message": "ok",
        "data": {"json_type": "orjson"}
    }
    return ORJSONResponse(content=orjson_content)


async def fake_streamer():
    for i in range(10):
        yield b"streaming fake bytes\n"


@app.get("/stream_demo")
async def stream_demo():
    return StreamingResponse(fake_streamer())


def iter_video(file_path):
    with open(file_path, mode="rb") as file:
        yield from file


@app.get("/stream_video_demo")
async def stream_video_demo():
    video_path = "res/demo.mp4"
    return StreamingResponse(iter_video(video_path), media_type="video/mp4")


@app.get("/file_demo")
async def file_demo():
    video_path = "res/demo.mp4"
    return FileResponse(path=video_path, filename="test.mp4", content_disposition_type="inline")


@app.get("/redirect_demo")
async def redirect_demo():
    return RedirectResponse(url="https://juejin.cn/user/817692384431470", status_code=301)


class UserModel(BaseModel):
    username: str = Field(description="用户名")
    age: int = Field(description="姓名")
    hobby: Optional[str] = Field(default="", description="爱好")


@app.get("/pydantic_model_demo", response_model=UserModel)
async def pydantic_model_demo():
    user_model = UserModel(
        username="hui",
        age=18,
        hobby="吃饭 睡觉 打游戏"
    )

    # user_info = dict(
    #     username="hui",
    #     hobby="吃饭 睡觉 打游戏"
    # )
    return user_model
    # return user_info


class UserOut(BaseModel):
    code: int = Field(default=0, description="响应码")
    message: str = Field(default="success", description="响应提示信息")
    data: UserModel = Field(description="响应数据")


@app.get("/pydantic_model_demo2", response_model=UserOut, summary="嵌套model")
async def pydantic_model_demo():
    user_model = UserModel(
        username="hui",
        age=18,
        hobby="吃饭 睡觉 打游戏"
    )

    return UserOut(data=user_model)


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
