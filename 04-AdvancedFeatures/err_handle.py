#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: err_handle.py
# @Desc: { 错误处理demo }
# @Date: 2024/05/21 11:07
from typing import Optional

import uvicorn
from fastapi import FastAPI, Request, Depends, Query
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from loguru import logger


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """全局异常处理"""
    if isinstance(exc, BizException):
        return JSONResponse(
            status_code=200,
            content={"code": exc.code, "msg": exc.msg, "data": {}}
        )
    elif isinstance(exc, RequestValidationError):
        return await request_validation_exception_handler(request, exc)
    else:
        logger.exception("Uncaught exception：sentry 告警 飞书通知")
        return JSONResponse(content={"code": 5000, "msg": "Internal Server Error", "data": {}}, status_code=500)


app = FastAPI(exception_handlers={Exception: global_exception_handler})
# app.add_exception_handler(Exception, global_exception_handler)


class BizException(Exception):
    def __init__(self, code=0, msg=""):
        self.code = code
        self.msg = msg


# @app.exception_handler(Exception)
# async def exception_handler(request: Request, exc: Exception):
#     return await global_exception_handler(request, exc)


class ErrorModel(BaseModel):
    error_num: int = Field(Query(description="错误编码"))
    error_msg: Optional[str] = Field(Query(description="错误信息"))


@app.get("/error_handle")
async def error_handle(req_model: ErrorModel = Depends(ErrorModel)):
    a = 1 / 0
    return req_model.model_dump()


@app.get("/biz_exception")
async def biz_exception():
    order_num = 0
    if order_num <= 0:
        raise BizException(msg="订单不足")

    order_num -= 1
    return order_num


def main():
    uvicorn.run(app)


if __name__ == '__main__':
    main()
