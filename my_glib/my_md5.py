#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/3/3 0:06
# @Author  : zhanhui
# @File    : my_md5.py


import hashlib
import os


def md5(md5_str):
    # Md5传入的字符串

    m = hashlib.md5(md5_str.encode(encoding="utf-8"))
    return m.hexdigest()


def md5_file(file_name):
    # Md5传入的文件

    real_file_name = os.path.realpath(file_name)
    if os.path.isfile(real_file_name):
        md5_obj = hashlib.md5()

        with open(real_file_name, 'rb') as f:
            md5_obj.update(f.read())
            hash_code = md5_obj.hexdigest()
            md5_code = str(hash_code).lower()

        return md5_code


def md5_big_file(file_name):
    # Md5大文件

    real_file_name = os.path.realpath(file_name)
    if os.path.isfile(real_file_name):
        md5_obj = hashlib.md5()

        with open(real_file_name, 'rb') as f:
            while True:
                d = f.read(8096)
                if not d:
                    break

                md5_obj.update(d)

            hash_code = md5_obj.hexdigest()
            md5_code = str(hash_code).lower()

        return md5_code


if __name__ == "__main__":
    file_name = r'my_md5.py'
    print(md5_file(file_name))
    print(md5_big_file(file_name))

    user_name = r'Deken'
    print(md5(user_name))
