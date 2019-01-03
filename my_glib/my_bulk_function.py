#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/6/4 23:18
# @Author  : zhanhui
# @File    : my_bulk_function.py


"""
    django的model批量新建/更新数据的方法。
"""


# 批量保存数据时，数据量最大值
MAX_CREATE_COUNT = 10000

# 批量更新数据时，数据量最大值
MAX_UPDATE_COUNT = 10000


def bulk_update(obj, primary_id, id_list, update_params=None):
    # 对传入的obj进行批量更新，返回更新的数据数量

    update_count = 0

    # 确保待更新的字段和值，是有效的字典结构，且有值。
    if not (isinstance(update_params, dict) and update_params):
        update_params = {"active": True}

    # 确保传入的是列表且不为空
    if isinstance(id_list, list) and id_list:
        try:
            # 查看传入的数据是否超过MAX_UPDATE_COUNT；超过的话需要对其进行拆分
            max_times, remainder = divmod(len(id_list), MAX_UPDATE_COUNT)
            if remainder > 0:
                max_times += 1

            if max_times:
                for i in range(max_times):
                    id_start = i * MAX_UPDATE_COUNT
                    id_end = (i + 1) * MAX_UPDATE_COUNT - 1

                    sub_id_list = id_list[id_start:id_end]

                    filter_params = {"%s__in" % primary_id: sub_id_list}
                    update_count += obj.objects.filter(**filter_params).update(**update_params)
        except Exception as e:
            print("批量更新失败！ class对象： %s，错误信息： %s" % (obj.__name__, e))

    return update_count


def bulk_save(obj, query_set_list, return_count=True):
    # 对传入的obj进行批量保存，返回保存的数据量

    save_count = 0
    create_list = []

    # 确保传入的是列表且不为空
    if isinstance(query_set_list, list) and query_set_list:
        try:
            create_list = obj.objects.bulk_create(query_set_list, batch_size=MAX_CREATE_COUNT)
            if create_list:
                save_count = len(create_list)
        except Exception as e:
            print("批量保存失败！ class对象： %s，错误信息： %s" % (obj.__name__, e))

    if return_count:
        return save_count
    else:
        return create_list
