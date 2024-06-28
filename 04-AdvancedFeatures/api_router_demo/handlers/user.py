#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: user.py
# @Desc: { 用户模块handler }
# @Date: 2024/06/28 11:58


class UserHandler:

    @classmethod
    async def register(cls, username: str, password: str):
        return "用户注册"

    @classmethod
    async def login(cls, username: str, password: str):
        return "用户登录"

    @classmethod
    async def get_user_detail(cls, user_id: int):
        return "获取用户详情"

    @classmethod
    async def get_users(cls, username: str):
        """获取用户列表"""
        # 参数校验
        # 调用业务层处理
        # 响应出参
        return "获取用户列表"
