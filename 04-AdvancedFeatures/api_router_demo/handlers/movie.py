#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: movie.py
# @Desc: { 电影模块handler }
# @Date: 2024/06/28 11:58


class MovieHandler:
    @classmethod
    async def get_movies(cls, movie_name: str, movie_type: str):
        """获取电影列表"""
        # 参数校验
        # 调用业务层处理
        # 响应出参
        return "获取电影列表"

    @classmethod
    async def get_movie_detail(cls, movie_id: int):
        return "获取电影详情"

