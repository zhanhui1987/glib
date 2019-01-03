#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/4/29 21:07
# @Author  : zhanhui
# @File    : my_psutil.py


"""
    脚本用于获取当前运行的pid，并根据传入的cmd_line返回其对应的pid列表
"""


import os
import subprocess
import psutil

from .my_time import now


def main():
    # 获取当前脚本的名称
    current_script_name = os.path.basename(__file__)

    # 设置cmd_line
    cmd_line_dict = {current_script_name: []}

    # 获取cmd_line对应的pid，此处传入cmd_line_eq为False，表明cmd_line_dict的键与获取的pid的cmd_line不要求完全一致，
    # 只要包含在其中即可。
    get_cmd_line_pids(cmd_line_dict, cmd_line_eq=False)
    print(cmd_line_dict)


def get_cmd_line_pids(cmd_line_dict, cmd_line_eq=True):
    # 需要传入cmd_line字典，其键为cmd_line，值为空数组；cme_line_eq表示pid的cmd_line是否与cmd_line字典的键完全一致
    # 获取到当前的pid和其cmd_line之后，将其与cmd_line字典进行对比，若cmd_line与cmd_line字典的键相等或包含在其中，则将
    # 对应的pid赋给cmd_line字典的值

    # 获取当前所有运行的pid
    current_pids = psutil.pids()

    for pid in current_pids:
        # 有一些进程，因权限限制，无法获取到其信息
        try:
            process = psutil.Process(pid)

            process_cmd_line_list = process.cmdline()
            process_cmd_line = " ".join(process_cmd_line_list)

            if process_cmd_line is not None:
                # 确认能够正确获取到process_cmd_line
                if cmd_line_eq:
                    # process_cmd_line需要与cmd_line字典中的值严格相等
                    if process_cmd_line in cmd_line_dict.keys():
                        cmd_line_dict[process_cmd_line].append(pid)
                else:
                    # process_cmd_line包含在cmd_line字典的值中就可以
                    for key in cmd_line_dict.keys():
                        if key in process_cmd_line:
                            cmd_line_dict[key].append(pid)
                            break
        except psutil.AccessDenied:
            pass
        except Exception as e:
            del e

    return cmd_line_dict


def kill_current_pids(pid_list):
    # 将传入的pid_list中所有的pid关闭

    if isinstance(pid_list, list):
        for pid in pid_list:
            # 会存在没有pid对应的权限的问题
            try:
                process = psutil.Process(pid)
                process.kill()
            except psutil.AccessDenied:
                pass


def execute_cmd_line(cmd_line):
    # 将传入的cmd_line进行启动

    if isinstance(cmd_line, str):
        cmd_list = cmd_line.split(" ")
        if cmd_list:
            print("[%s] 执行cmd_line : %s" % (now(), " ".join(cmd_list)))

            subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)


def is_running(script_name):
    # 检测传入的脚本是否在运行中

    running = False

    cmd_line_dict = {
        script_name: [],
    }

    cmd_line_pids_dict = get_cmd_line_pids(cmd_line_dict, cmd_line_eq=False)
    if script_name in cmd_line_pids_dict.keys() and len(cmd_line_pids_dict[script_name]) > 1:
        running = True

    return running


if __name__ == "__main__":
    main()
