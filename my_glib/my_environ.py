#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/6/6 10:40
# @Author  : Zhanhui
# @File    : my_environ.py


"""
    从环境变量中获取指定的值。
"""


import os


def get_environ(environ_key):
    # 从环境变量中获取指定字段的值

    return os.environ.get(environ_key)


if __name__ == "__main__":
    key = "PYTHONPATH"
    print(get_environ(key))
