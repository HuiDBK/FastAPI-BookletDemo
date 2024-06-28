#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: user.py
# @Desc: { 用户模块路由 }
# @Date: 2024/06/28 11:47
from fastapi import APIRouter
from handlers import UserHandler

user_router = APIRouter()

user_router.add_api_route(
    "/api/v1/users/register", UserHandler.register, methods=["POST"], summary="用户注册"
)
user_router.add_api_route(
    "/api/v1/users/login", UserHandler.login, methods=["POST"], summary="用户登陆"
)
user_router.add_api_route(
    "/api/v1/users", UserHandler.get_users, methods=["GET"], summary="获取用户列表"
)
user_router.add_api_route(
    "/api/v1/users/{user_id}", UserHandler.get_user_detail, methods=["GET"], summary="用户详情"
)
