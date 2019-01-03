#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/6/26 13:39
# @Author  : Zhanhui
# @File    : my_doc2pdf.py


"""
    将传入的word文件转换成pdf文件
"""


import os
import pythoncom

from zipfile import ZipFile
from win32com.client import Dispatch, constants, gencache


def doc2pdf(word_file_path, pdf_file_path):
    # 将传入的word文件转换成pdf文件，并保存到传入的pdf文件路径中

    # 获取真实路径
    real_word_file_path = os.path.realpath(word_file_path)
    real_pdf_file_path = os.path.realpath(pdf_file_path)

    # 判断word文件存在
    if os.path.isfile(os.path.realpath(real_word_file_path)):
        # 判断word文件是正确的docx类型
        if _is_docx_file(real_word_file_path):
            error_msg = _convert_and_save_file(real_word_file_path, real_pdf_file_path)
        else:
            error_msg = "Word文件： %s 不是正确的docx格式！" % real_word_file_path
    else:
        error_msg = "Word文件： %s 不存在！" % real_word_file_path

    return error_msg


def _is_docx_file(word_file_path):
    # 判断传入的文件是否是docx文件

    is_docx_file = False

    # docx实质上是一个zip压缩包，可以查看其中是否包含：word/document.xml来判断文件是否是docx文件
    zip_file = ZipFile(word_file_path)

    if zip_file.namelist().__contains__("word/document.xml"):
        is_docx_file = True

    return is_docx_file


def _convert_and_save_file(real_word_file_path, real_pdf_file_path):
    # 转换并保存文件

    error_msg = None

    # 初始化环境
    pythoncom.CoInitialize()
    gencache.EnsureModule('{00020905-0000-0000-C000-000000000046}', 0, 8, 4)

    word_obj = Dispatch("Word.Application")
    try:
        # 打开word文件
        doc_obj = word_obj.Documents.Open(real_word_file_path, ReadOnly=1)

        # 转换成pdf文件并保存
        doc_obj.ExportAsFixedFormat(real_pdf_file_path, constants.wdExportFormatPDF,
                                    Item=constants.wdExportDocumentWithMarkup,
                                    CreateBookmarks=constants.wdExportCreateHeadingBookmarks)
    except Exception as e:
        error_msg = "转换成PDF文件失败： %s" % e
    finally:
        word_obj.Quit(constants.wdDoNotSaveChanges)

    if not os.path.isfile(real_pdf_file_path):
        error_msg = "保存PDF文件失败！"

    return error_msg
