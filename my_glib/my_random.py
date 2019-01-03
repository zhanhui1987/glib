#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/2/15 0:12
# @Author  : Zhanhui
# @File    : my_random.py


# 生成指定长度的随机数字或字符。

import random
import string


def get_random_int(int_len=1):
    if isinstance(int_len, int):
        source = [str(i) for i in range(10)]
        return _get_random(source, int_len)


def get_random_char(char_len=1):
    if isinstance(char_len, int):
        source = list(string.ascii_letters)
        source.extend([str(i) for i in range(10)])

        return _get_random(source, char_len)


def _get_random(source, len):
    random_list = list()

    for i in range(len):
        random_list.extend(random.sample(source, 1))

    return "".join(random_list)


if __name__ == "__main__":
    char_len = 5

    print(get_random_int(char_len))
    print(get_random_char(char_len))
