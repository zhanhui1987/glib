#!/usr/bin/env python
# coding: utf-8

# @Time    : 2018/3/20 10:27
# @Author  : Zhanhui
# @File    : my_ip_list.py


import netaddr

from IPy import IP


def get_ip_list(ip):
    # 将传入的ip按照ip段或者ip范围进行处理，返回其ip列表

    ip_list = []
    error_msg = None

    try:
        if "-" in ip:
            ip_list, error_msg = _segment_to_list(ip)
        elif "/" in ip:
            ip_list = _mask_to_list(ip)
        else:
            if _check_ip_format(ip):
                ip_list = [ip]
            else:
                error_msg = "传入了错误的IP： %s" % ip
    except Exception as e:
        del e
        error_msg = "获取IP列表失败： %s" % ip

    return ip_list, error_msg


def get_ip_segment(start_ip, end_ip):
    # 将传入的开始IP和结束IP，转换成相应的IP段

    ip_segment_list = list()
    error_msg = None

    if _check_ip_format(start_ip) and _check_ip_format(end_ip):
        ip_segment_list.append(str(IP("%s-%s" % (start_ip, end_ip), make_net=True)))
    else:
        error_msg = "传入了错误的IP： %s - %s" % (start_ip, end_ip)

    return ip_segment_list, error_msg


def get_ip_cidrs(start_ip, end_ip):
    # 根据传入的开始IP和结束IP，获取IP段列表

    ip_cidrs_list = list()
    error_msg = None

    if _check_ip_format(start_ip) and _check_ip_format(end_ip):
        cidrs = netaddr.iprange_to_cidrs(start_ip, end_ip)
        ip_cidrs_list = [str(c) for c in cidrs]
    else:
        error_msg = "传入了错误的IP： %s - %s" % (start_ip, end_ip)

    return ip_cidrs_list, error_msg


def _ip2num(ip):
    # 将ip转换成数字

    ips = [int(x) for x in ip.split('.')]
    return ips[0] << 24 | ips[1] << 16 | ips[2] << 8 | ips[3]


def _num2ip(num):
    # 将数字转换成ip

    return "%s.%s.%s.%s" % ((num >> 24) & 0xff, (num >> 16) & 0xff, (num >> 8) & 0xff, num & 0xff)


def _segment_to_list(ip_segment):
    # 将传入的ip范围转换成ip列表

    ip_list = []
    error_msg = None

    # 将ip范围进行分解
    segment_list = ip_segment.split("-")
    if len(segment_list) == 2:
        ip_start_list = segment_list[0].split(".")
        ip_end_list = segment_list[1].split(".")

        ip_start = _ip2num(".".join(ip_start_list))
        if len(ip_end_list) == 4:
            ip_end_new_list = ip_end_list
            ip_end = _ip2num(".".join(ip_end_new_list))
        else:
            ip_end_new_list = ip_start_list[:3]
            ip_end_new_list.extend(ip_end_list)
            ip_end = _ip2num(".".join(ip_end_new_list))

        # 检查拆分成列表的IP是否是正确的IP
        if _check_ip_list_format(ip_start_list) and _check_ip_list_format(ip_end_new_list):
            ip_list = [_num2ip(num) for num in range(ip_start, ip_end + 1) if num & 0xff]
        else:
            print("传入了错误的IP： %s" % ip_segment)
    else:
        error_msg = "传入了错误的IP范围： %s" % ip_segment

    return ip_list, error_msg


def _mask_to_list(ip_mask):
    # 将传入的带掩码的ip转换成ip列表

    return [str(ip) for ip in IP(ip_mask, make_net=True)]


def _check_ip_format(ip):
    # 检测传入的ip是否是正确的IP格式

    check = False

    try:
        IP(ip)
        check = True
    except Exception as e:
        del e

    return check


def _check_ip_list_format(ip_list):
    # 检查传入的拆分成列表格式的IP是否是正确的IP

    return _check_ip_format(".".join(ip_list))


def main():
    ip_list = ["119.97.172.1-119.97.172.1321"]

    for origin_ips in ip_list:
        print(get_ip_list(origin_ips))

    print(_check_ip_format("119.97.172.1321"))

    # 获取IP段列表
    start_ip = "119.97.172.1"
    end_ip = "119.97.172.35"
    print(get_ip_cidrs(start_ip, end_ip))


if __name__ == "__main__":
    main()
