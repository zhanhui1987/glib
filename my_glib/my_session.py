#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/7/30 15:30
# @Author  : Zhanhui
# @File    : my_session.py


def set_session(request, session_name, session_value):
    """
        在request中设置指定session名称的值
    :param request: url请求对象
    :param session_name: session名称
    :param session_value: session值
    :return: True / False
    """

    success = False

    if request and session_name and session_value:
        try:
            request.session[session_name] = session_value
            success = True
        except Exception as e:
            del e

    return success


def get_session(request, session_name):
    """
        从request中取出指定的session值
    :param request: url请求对象
    :param session_name: session名称
    :return: session_value: session值
    """

    session_value = None

    if request and session_name:
        session_value = request.session.get(session_name)

    return session_value


def del_session(request, session_name):
    """
        将request中指定的seesion_name删除
    :param request: url请求对象
    :param session_name: session名称
    :return: True / False
    """

    success = False

    if request and session_name:
        if session_name in request.session.keys():
            del request.session[session_name]

        if session_name not in request.session.keys():
            success = True

    return success


def set_sessions(request, session_list):
    """
        批量设置session
    :param request: 请求对象
    :param session_list: 待设置的session列表，列表中每个字典都应包含两个值：name-待设置的session名称，value-待设置的session值
    :return:
    """

    if request and isinstance(session_list, list):
        for row in session_list:
            if isinstance(row, dict):
                session_name = row.get("name")
                session_value = row.get("value")

                if session_name and session_value:
                    set_session(request, session_name, session_value)


def bulk_get_session(request, session_name_list):
    """
        批量获取session值
    :param request: 请求对象
    :param session_name_list: 需获取的session名称的列表
    :return: session_dict： 以session名称为键，session值为值的session字典
    """

    session_dict = {}

    if request and isinstance(session_name_list, list) and session_name_list:

        for session_name in session_name_list:
            session_dict[session_name] = get_session(request, session_name)

    return session_dict


def bulk_del_session(request, session_name_list):
    """
        批量删除session
    :param request: 请求对象
    :param session_name_list: 待删除的session名称的列表
    :return:
    """
    if request and isinstance(session_name_list, list) and session_name_list:
        for session_name in session_name_list:
            del_session(request, session_name)


def extract_session(request, session_name):
    """
        从session中提取指定名称的session值，提取成功之后将session中的数据删除
    :param request: 请求对象
    :param session_name: 待提取的session名称
    :return: session值
    """

    session_value = get_session(request, session_name)
    if session_value is not None:
        del_session(request, session_name)
    return session_value
