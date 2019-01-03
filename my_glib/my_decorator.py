#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/7/20 15:59
# @Author  : Zhanhui
# @File    : my_decorator.py


"""
    封装常用的装饰器。
"""


import time

from functools import wraps


def func_cost(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func_result = func(*args, **kwargs)
        end_time = time.time()

        print("%s cost time: %.2f" % (func.__name__, end_time - start_time))
        return func_result
    return wrapper
