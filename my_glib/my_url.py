#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2019/3/13 14:52
# @Author  : Zhanhui
# @File    : my_url.py


from django.core.validators import URLValidator


def check_valid_url(url):
    """
    检测传入的url是否正确的格式。
    :param url:
    :return:
    """

    check = False

    try:
        val_obj = URLValidator()
        val_obj(url)
    except Exception as e:
        del e

    return check
