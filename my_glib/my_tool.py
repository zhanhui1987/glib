#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/5/9 0:32
# @Author  : zhanhui
# @File    : my_tool.py


"""
    本包主要用于封装django views.py中常用的一些函数。
"""


import json
import time
import os

from django.core.files.uploadedfile import TemporaryUploadedFile
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse


def init_response_data(list_field=None, dict_field=None, zero_field=None):
    # 初始化页面返回的数据。list_field用于接受需要其初始化为空数组的字段，用英文","连接多个字段；dict_field
    # 用于接受需要初始化为空字段的字段，用英文","连接多个字段;zero_field用于接受需初始化为0的字段，用英文","连接多个字段

    response_data = {"results": [], "results_count": 0, "data": {}, "error_msg": "", "success": 0}

    # 将list_field传入的字段初始化为空数组
    if list_field is not None:
        for field in list_field.split(","):
            response_data[field] = []

    # 将dict_field传入的字段初始化为空字典
    if dict_field is not None:
        for field in dict_field.split(","):
            response_data[field] = dict()

    # 将zero_field传入的字段初始化为0
    if zero_field is not None:
        for field in zero_field.split(","):
            response_data[field] = 0

    return response_data


def get_choice_map(choice):
    # 将models中定义的CHOICES，转换成dict结构

    choice_dict = dict()

    # choice应该是元组结构，其中包含了多个小元组，每一个小元组都应包含两个元素，第一个作为键，第二个作为值
    if isinstance(choice, tuple):
        for row in choice:
            if isinstance(row, tuple) and len(row) == 2:
                choice_dict[row[0]] = row[1]

    return choice_dict


def get_selection_choice_list(choice, is_filter=False, has_default=False, filter_choice_list=None):
    # 将models中定义的CHOICES，转换成list结构，其中每一个元素为一个字典，保存CHOICES中每一项的数据库值和显示值

    choice_list = list()

    # 若没有传入需忽略的choice，则将其设置为空列表
    if not isinstance(filter_choice_list, list) or not filter_choice_list:
        filter_choice_list = list()

    if isinstance(choice, tuple):
        for row in choice:
            if isinstance(row, tuple) and len(row) == 2:
                selection_data = {
                    "db_value": str(row[0]),
                    "show_value": row[1],
                }

                # 查看是否有需要保留的字段
                if filter_choice_list:
                    if str(row[0]) in filter_choice_list:
                        choice_list.append(selection_data)
                else:
                    choice_list.append(selection_data)

    # 若有获取到的list
    if choice_list:
        if is_filter:
            # 若是过滤列表，则应将默认的全部选项添加进去
            choice_list.insert(0, {"db_value": "all", "show_value": "全部"})
        elif has_default:
            # 若是选择列表，则应将默认的空数据添加进去
            choice_list.insert(0, {"db_value": "", "show_value": "请选择"})

    return choice_list


def set_field_detail(data, field, detail_map=None, choice=None, delete_origin_key=False, replace_origin_str=False):
    # 将数据库中一些choice类型的数据，转换成页面显示的样式（通过设置detail的方式来实现）

    if isinstance(data, dict):
        if detail_map is None and choice is not None:
            detail_map = get_choice_map(choice)

        filed_value = data.get(field)
        if isinstance(detail_map, dict) and filed_value is not None:
            # 查看是否需要将原始值进行替换，还是重新赋新的值
            if replace_origin_str:
                data[field] = detail_map.get(filed_value) or filed_value
            else:
                data["%s_detail" % field] = detail_map.get(filed_value) or filed_value

            # 获取到显示用的值之后，查看是否需要将原始键删除
            if delete_origin_key:
                del data[field]


def init_api_response_data():
    # 初始化api的返回数据

    response_data = {
        "data": [],
        "code": 0,
        "error_msg": None,
        "total": 0,
        "cost": 0,
        "_start_time": time.time()
    }

    return response_data


def caculate_api_cost(response_data):
    # 计算api耗时

    try:
        response_data["cost"] = "%.2f" % (time.time() - response_data["_start_time"])
        del response_data["_start_time"]
    except (KeyError, ValueError):
        pass


def get_int_param_from_request(param_value, default_value=0):
    # 获取并确保从request传入的参数是正常的int类型

    try:
        param_value = int(param_value)
    except (ValueError, TypeError):
        param_value = default_value

    return param_value


def get_page_start_and_end(request, page_no=1, page_size=30):
    # 根据传入的页码和每页数量，获取数据的开始和结束位置

    # 从request中获取传入的页码和每页数量，并确保其是正常的int类型
    page_no = get_int_param_from_request(request.GET.get("page"), default_value=page_no)
    page_size = get_int_param_from_request(request.GET.get("size"), default_value=page_size)

    # 获取开始和结束位置
    try:
        page_start = (page_no - 1) * page_size
        page_end = page_no * page_size

        if page_start < 0:
            page_start = 0
        if page_end < 0:
            page_end = 0
    except ValueError:
        page_start = 0
        page_end = 0

    return page_start, page_end


def get_boolean_param_from_request(request, key, default_value=0):
    # 从request中读取指定key的值，并将其转换成int，再转换成boolean值

    # 从request中取出指定key对应的值，并将其转换成int
    try:
        value = int(request.POST.get(key))
    except (TypeError, ValueError):
        value = default_value

    # 将获取到的value值转换成boolean值
    if value:
        return True
    else:
        return False


def get_boolean_param_from_json_data(received_json_data, key, default_value=False):
    # 从获取到的json格式的数据中，获取指定字段的boolean值

    # 从传入的json数据中，获取指定键的值
    try:
        value = int(received_json_data.get(key))
    except (TypeError, ValueError):
        value = default_value

    # 将获取到的value值转换成boolean值
    if value:
        return True
    else:
        return False


def get_choice_value_list(choice, is_filter=False):
    # 从传入的choice定义中，获取字段可取得的值列表

    value_list = []

    if isinstance(choice, tuple):
        for row in choice:
            if isinstance(row, tuple) and len(row) == 2:
                value_list.append(str(row[0]))

    # 若获取的是过滤用的choice_list，则需要在列表的开始添加“all”
    if is_filter:
        value_list.insert(0, "all")

    return value_list


def check_value_in_choice_value_list(value, choice):
    # 检查传入的值是否在传入的choice的值中

    check = False

    value_list = get_choice_value_list(choice)
    if value in value_list:
        check = True

    return check


def dict_filter(origin_dict, reserved_keys):
    # 对传入的字典进行处理，保留传入的字段，其余字段都删除

    new_dict = dict()

    if isinstance(origin_dict, dict) and isinstance(reserved_keys, list):
        # 查看需要保留的字段是否在原始字典中，若在的话则将其键、值赋给新字典
        for key in origin_dict.keys():
            if key in reserved_keys:
                new_dict[key] = origin_dict[key]

    return new_dict


def upload_file(file_obj, save_root_path, file_name_extra_prefix=None):
    # 上传文件到指定的目录中。file_name_extra_prefix表示在保存文件时，在文件名中添加的额外的前缀。

    origin_file_name = None
    real_save_file_path = None
    error_msg = None

    # 确保获取到的文件对象是正确的文件对象
    if isinstance(file_obj, TemporaryUploadedFile):
        # 获取上传文件的文件名
        origin_file_name = file_obj.name
        if origin_file_name is not None:
            # 查看是否有额外的前缀需要添加到文件名中
            if file_name_extra_prefix is not None:
                save_file_name = "%s.%s" % (file_name_extra_prefix, origin_file_name)
            else:
                save_file_name = origin_file_name

            # 检查保存的目录是否存在，不存在的话，需要将其创建
            real_file_dir_path = os.path.realpath(save_root_path)
            if not os.path.isdir(real_file_dir_path):
                os.makedirs(real_file_dir_path)

            # 确保保存文件不存在，若存在的话，将其删除
            real_save_file_path = os.path.realpath(os.path.join(real_file_dir_path, save_file_name))
            if os.path.isfile(real_save_file_path):
                os.remove(real_save_file_path)

            # 将file_obj中的内容写入到指定的保存文件中
            with open(real_save_file_path, 'wb') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
        else:
            error_msg = "无法获取上传的文件名！"
    else:
        error_msg = "无法获取上传文件！"

    # 若有报错，且文件已上传，则应将文件删除
    if error_msg is not None and real_save_file_path is not None and os.path.isfile(real_save_file_path):
        os.remove(real_save_file_path)

    return origin_file_name, real_save_file_path, error_msg


def get_json_data_from_body(request):
    # 从request的body中，读取传递过来的json数据

    received_json_data = dict()

    # 获取json数据
    if isinstance(request, WSGIRequest):
        body_data = request.body.decode("utf-8")

        if body_data:
            try:
                received_json_data = json.loads(body_data)
            except Exception as e:
                del e

    return received_json_data


def get_param_value_from_body(request, param):
    # 从request的body中，读取传递过来的json数据，并提取指定参数的值

    value = None

    if param:
        received_json_data = get_json_data_from_body(request)
        value = received_json_data.get(param)

    return value


def process_return(response_data):
    # 将每个response_data进行反馈，并计算其耗时

    # 计算api耗时
    caculate_api_cost(response_data)

    return JsonResponse(response_data)
