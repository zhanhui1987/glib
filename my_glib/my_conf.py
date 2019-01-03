#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/3/2 20:45
# @Author  : zhanhui
# @File    : my_conf.py


import configparser
import os

from collections import defaultdict


class ConfFile(object):
    """
       从配置文件中读取各配置
    """

    def __init__(self, conf_file):
        self._conf_file = os.path.realpath(conf_file)
        self._get_conf_dict()

    def _get_conf_dict(self):
        # 从配置文件中获取配置字典

        cp = configparser.ConfigParser()
        self.conf_dict = defaultdict(dict)

        if os.path.isfile(self._conf_file):
            cp.read(self._conf_file, encoding="utf-8")

            try:
                for section in cp.sections():
                    for option in cp.options(section):
                        try:
                            option = int(option)
                        except Exception as e:
                            del e
                        self.conf_dict[section][option] = cp.get(section, option)
            except Exception as e:
                del e
        else:
            print("配置文件不存在 : %s" % self._conf_file)

    def get_param(self, section, option):
        try:
            return self.conf_dict.get(section).get(option)
        except Exception as e:
            del e
            return None


def get_int_option(option_value, default_value=0):
    # 将传入的配置文件的值，从str转换成int；若获取的值为None或转换失败，则将其值设置为默认值：0

    option_int_value = default_value

    try:
        option_int_value = int(option_value)
    except ValueError:
        pass

    return option_int_value


if __name__ == "__main__":
    test_conf_file = "test_conf_file.ini"
    cf = ConfFile(test_conf_file)

    c_dict = cf.conf_dict
    print(c_dict)

    database = cf.get_param("central", "database")
    print(database)
