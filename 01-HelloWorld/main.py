#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @Desc: { fastapi hello world 案例 }
# @Date: 2023/08/06 22:16
import uvicorn
from fastapi import FastAPI

app = FastAPI(description="hello world")


@app.get(path="/", summary="首页")
def index():
    return "index"


@app.get(path="/hello", summary="您好")
def hello():
    return "hello world"


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
