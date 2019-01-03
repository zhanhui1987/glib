#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/11/15 15:17
# @Author  : Zhanhui
# @File    : my_zip.py


"""
生成压缩.zip文件。
"""


import os
import zipfile


def zip_dir(dir_path, zip_file_path, check_file_dict=None):
    """
    压缩文件夹，传入待压缩的文件夹目录及生成压缩文件的路径。
    只压缩传入目录中的文件，对目录中的子目录不做处理。
    :return:
    """

    error_msg = None

    if check_file_dict is None:
        check_file_dict = dict()

    # 默认生成的zip文件位于待压缩的目录中
    if os.path.isdir(os.path.realpath(dir_path)) and zip_file_path:
        if not zip_file_path.endswith(".zip"):
            zip_file_path = "%s.zip" % zip_file_path

        # 创建zip文件对象
        zip_obj = zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED)

        # 统计待压缩和压缩成功的文件数量
        file_count = 0
        compress_file_count = 0

        try:
            for path, dir_name_list, file_name_list in os.walk(dir_path):
                for file_name in file_name_list:
                    file_path = os.path.realpath(os.path.join(path, file_name))

                    # 检测文件是否和生成的压缩文件是同一个文件，是的话，不应将其进行压缩处理
                    if os.path.isfile(file_path) and file_path != zip_file_path:
                        file_count += 1

                        # 获取压缩包中文件的路径，应将path去除
                        f_path = file_path.replace(dir_path, "")

                        try:
                            zip_obj.write(file_path, f_path)
                            compress_file_count += 1
                        except Exception as e:
                            del e
        except Exception as e:
            del e
        finally:
            zip_file_list = [o.filename for o in zip_obj.filelist]
            zip_obj.close()

        # 判断是否需要将生成的压缩文件删除。若待压缩文件夹为空文件夹，则不应删除生成的空压缩文件（意味着压缩操作是成功的）；若待压缩
        # 文件夹不为空，但是压缩成功的文件数量为0，则需要删除生成的压缩文件（压缩操作不成功）
        if file_count:
            if not compress_file_count:
                _remove_zip_file(zip_file_path)

        # 检查需要的检验的文件是否都成功压缩
        if zip_file_list:
            for zip_file in zip_file_list:
                if zip_file in check_file_dict.keys():
                    del check_file_dict[zip_file]

        if check_file_dict:
            error_msg = "以下文件未成功压缩：%s" % "，".join(check_file_dict.keys())
            _remove_zip_file(zip_file_path)

    return error_msg


def _remove_zip_file(zip_file_path):
    """
    生成压缩文件失败，需要将其清理掉
    :return:
    """

    if os.path.isfile(zip_file_path):
        try:
            os.remove(zip_file_path)
        except Exception as e:
            del e


if __name__ == "__main__":
    zip_dir_path = os.path.realpath("")
    zip_dir(zip_dir_path, "my_lib")
