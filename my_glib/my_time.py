#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/3/2 23:37
# @Author  : zhanhui
# @File    : my_time.py


import calendar
import datetime
import time


def _local_time():
    return time.localtime(time.time())


def _format_time(format_str):
    return time.strftime(format_str, _local_time())


def now():
    # 当前时间
    return _format_time("%Y/%m/%d %H:%M:%S")


def today():
    # 当前日期
    return _format_time("%Y/%m/%d")


def today2():
    # 另外一种格式的当前日期
    return _format_time("%Y-%m-%d")


def today3():
    return _format_time("%Y.%m.%d")


def current_month():
    # 当前月
    return _format_time("%m")


def current_year():
    # 当前年
    return _format_time("%Y")


def first_day_of_curmonth():
    # 当前月的第一天
    return _format_time("%Y-%m-01")


def last_day_of_curmonth():
    # 当前月的最后一天
    cur_year = current_year()
    cur_month = current_month()
    last_day = calendar.monthrange(int(cur_year), int(cur_month))[1]
    return "%s-%s-%s" % (current_year(), current_month(), last_day)


def is_valid_date(date_string):
    # 判断传入的字符串是否是有效的日期

    is_valid = True

    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
    except (ValueError, TypeError):
        is_valid = False

    return is_valid


if __name__ == "__main__":
    print("now: %s" % now())
    print("curdate: %s" % today())
    print("curdate2: %s" % today2())
    print("curyear: %s" % current_year())
    print("curmonth: %s" % current_month())
    print("first day of curmonth: %s" % first_day_of_curmonth())
    print("last day of curmonth: %s" % last_day_of_curmonth())
