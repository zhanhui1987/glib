#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/6/5 13:04
# @Author  : Zhanhui
# @File    : my_ip.py


"""
    与IP相关的一些方法。
"""


import IPy
import socket


def check_valid_ip(ip):
    # 检查传入的ip是否是正确的格式

    check = False

    if ip is not None:
        ip = ip.strip()
        try:
            socket.inet_aton(ip)
            check = True
        except Exception as e:
            del e

    return check


def check_valid_ip2(ip):
    """
    检测传入的ip是否正确格式
    :param ip:
    :return:
    """

    check = False

    try:
        IPy.IP(ip)
    except Exception as e:
        del e

    return check
