#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/7/31 9:44
# @Author  : Zhanhui
# @File    : my_cookie.py


SESSION_COOKIE_AGE = 30  # 30 seconds


def get_cookie(request, cookie_name):
    """
        从request中获取指定cookie名称的值
    :param request: 请求对象
    :param cookie_name: 需获取值的cookie名称
    :return: cookie_value： 获取到的值
    """

    cookie_value = None

    if request and cookie_name:
        try:
            cookie_value = request.COOKIES.get(cookie_name)
        except Exception as e:
            del e

    return cookie_value


def set_cookie(response, cookie_name, cookie_value, expire=SESSION_COOKIE_AGE):
    """
        设置cookie
    :param response: 响应对象
    :param cookie_name: cookie名称
    :param cookie_value: cookie值
    :param expire: cookie有效期（单位：秒）
    :return:
    """

    if response and cookie_name and cookie_value:
        if not isinstance(expire, int):
            expire = SESSION_COOKIE_AGE

        try:
            response.set_cookie(cookie_name, cookie_value, expire)
        except Exception as e:
            del e


def del_cookie(response, cookie_name):
    """
        删除cookie
    :param response: 响应对象
    :param cookie_name: 待删除的cookie的名称
    :return:
    """

    if response and cookie_name:
        try:
            response.delete_cookie(cookie_name)
        except Exception as e:
            del e


def get_cookies(request, cookie_name_list):
    """
        批量获取cookie
    :param request: 请求对象
    :param cookie_name_list: 待批量获取的cookie名称的列表
    :return: cookie_dict: 获取到的cookie的名称-值的字典
    """

    cookie_dict = dict()
    if request and isinstance(cookie_name_list, list) and cookie_name_list:
        for cookie_name in cookie_name_list:
            cookie_dict[cookie_name] = get_cookie(request, cookie_name)

    return cookie_dict


def bulk_set_cookie(response, cookie_list):
    """
        批量设置cookie
    :param response: 响应对象
    :param cookie_list: 待批量设置的cookie信息列表，列表中每个字典中的值：
                        name: cookie名称
                        value: cookie值
                        expire: cookie有效期
    :return:
    """

    if response and isinstance(cookie_list, list) and cookie_list:
        for row in cookie_list:
            if isinstance(row, dict):
                cookie_name = row.get("name")
                cookie_value = row.get("value")
                expire = row.get("expire", 3600)

                if cookie_name is not None and cookie_value is not None and isinstance(expire, int):
                    set_cookie(response, cookie_name, cookie_value, expire)


def bulk_del_cookie(response, cookie_name_list):
    """
        批量删除cookie
    :param response: 响应对象
    :param cookie_name_list: 待删除的cookie名称列表
    :return:
    """

    if response and isinstance(cookie_name_list, list) and cookie_name_list:
        for cookie_name in cookie_name_list:
            del_cookie(response, cookie_name)
