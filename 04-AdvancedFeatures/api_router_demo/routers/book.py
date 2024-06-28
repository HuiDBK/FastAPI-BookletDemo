#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: book.py
# @Desc: { 书籍模块路由 }
# @Date: 2024/06/28 11:48
from fastapi import APIRouter
from handlers import BookHandler

book_router = APIRouter()

book_router.add_api_route(
    "/api/v1/books", BookHandler.get_books, methods=["GET"], summary="获取图书列表"
)
book_router.add_api_route(
    "/api/v1/books/{book_id}", BookHandler.get_book_detail, methods=["GET"], summary="图书详情"
)
