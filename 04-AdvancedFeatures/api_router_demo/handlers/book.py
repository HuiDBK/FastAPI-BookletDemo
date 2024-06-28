#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: book.py
# @Desc: { 图书模块handler }
# @Date: 2024/06/28 11:58

class BookHandler:
    @classmethod
    async def get_books(cls, book_name: str):
        """获取图书列表"""
        # 参数校验
        # 调用业务层处理
        # 响应出参
        return "获取图书列表"

    @classmethod
    async def get_book_detail(cls, book_id: int):
        return "获取图书详情"
