#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: __init__.py.py
# @Desc: { 项目路由初始化模块 }
# @Date: 2024/06/28 11:47
from fastapi import APIRouter
from .book import book_router
from .user import user_router
from .movie import movie_router

api_router = APIRouter()

api_router.include_router(user_router, tags=["用户模块"])
api_router.include_router(book_router, tags=["图书模块"])
api_router.include_router(movie_router, tags=["电影模块"])
