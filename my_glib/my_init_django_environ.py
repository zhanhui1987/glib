#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/5/31 17:46
# @Author  : Zhanhui
# @File    : my_init_django_environ.py


"""
    初始化django环境，以方便在脚本中调用django的model。
"""


import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
django.setup()
