#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: movie.py
# @Desc: { 电影模块路由 }
# @Date: 2024/06/28 11:48
from fastapi import APIRouter
from handlers import MovieHandler

movie_router = APIRouter()

movie_router.add_api_route(
    "/api/v1/movies", MovieHandler.get_movies, methods=["GET"], summary="获取电影列表"
)
movie_router.add_api_route(
    "/api/v1/movies/{movie_id}", MovieHandler.get_movie_detail, methods=["GET"], summary="电影详情"
)
