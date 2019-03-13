#!/usr/bin/env python
# coding: utf-8

# @Time    : 2018/5/2 14:49
# @Author  : Zhanhui
# @File    : my_domain.py


import idna
import re
import socket
import tldextract

from tldextract.tldextract import ExtractResult


def main():
    domain = "www.baidu.com.cn/as.com"

    top_domain = get_top_domain(domain)
    print(top_domain)


def get_top_domain(domain):
    """
    获取传入域名的主域名
    :param domain: A domain.
    :return: Top_domain of the param domain.
    """

    top_domain = None

    if domain is not None:
        # 对domain进行处理：转成小写、去掉前后的多余字符、中文域名的转换等
        domain = _translate(domain)

        if check_valid_ip(domain):
            top_domain = domain
        elif "," in domain:
            # 检测域名中是否包含有 ","
            pass
        else:
            extract_obj = tldextract.extract(domain)

            if isinstance(extract_obj, ExtractResult) and extract_obj.domain and extract_obj.suffix:
                top_domain = "%s.%s" % (extract_obj.domain, extract_obj.suffix)

        # 判断域名中间是否有ip，用来处理类似于： https://10.10.10.10/admin 等形式的域名
        if top_domain is None:
            ip_list = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", domain)
            if ip_list:
                top_domain = ip_list[0]

    return top_domain


def _translate(domain):
    # 对domain进行处理：转成小写、去掉前后的多余字符、中文域名的转换等

    # 将传入的域名转换成小写
    domain = domain.lower()

    # 将传入的域名去掉多余的字符
    domain = domain.strip()
    domain = domain.expandtabs()  # 将tab替换为空格
    domain = domain.replace(" ", "")  # 将空格删除

    # 对中文域名进行转换
    if "xn--" in domain:
        # 将punycode转换成中文
        domain = idna.decode(domain)

    return domain


def decode_punycode(domain):
    """
    检测传入的域名是否是punycode编码格式，是的话，将其转换成对应的中文域名
    :return:
    """

    convert_domain = domain

    # 对中文域名进行转换
    if "xn--" in domain:
        # 将punycode转换成中文
        convert_domain = idna.decode(domain)

    return convert_domain


def check_valid_ip(ip):
    # 检查传入的ip是否是正确的格式

    is_valid_ip = False

    if ip is not None:
        ip = ip.strip()
        try:
            socket.inet_aton(ip)
            is_valid_ip = True
        except Exception as e:
            del e

    return is_valid_ip


def is_valid_domain(domain):
    """
    检测传入的domain是否是正确的主域名格式。
    :param domain: 待检测的主域名
    :return:
    """

    check = False

    top_domain = get_top_domain(domain)
    if top_domain == domain:
        check = True

    return check


if __name__ == "__main__":
    main()
