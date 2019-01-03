#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/6/5 13:04
# @Author  : Zhanhui
# @File    : my_ip.py


"""
    与IP相关的一些方法。
"""


import socket


def check_valid_ip(ip):
    # 检查传入的ip是否是正确的格式

    is_valid_ip = False

    if ip is not None:
        ip = ip.strip()
        try:
            socket.inet_aton(ip)
            is_valid_ip = True
        except Exception as e:
            del e

    return is_valid_ip
