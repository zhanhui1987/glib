#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/8/31 16:15
# @Author  : Zhanhui
# @File    : my_page.py


from django.core.handlers.wsgi import WSGIRequest


class Page(object):
    def __init__(self, request=None, page=1, size=30):
        """
        根据传入的 request 或 page和size，获取分页数据：page_start和page_end
        :param request: 请求对象，应是 rest_framework.request.Request 类型
        :param page: 页码数，默认为1
        :param size: 每页数据量，默认为30
        """

        # 初始化默认属性
        self._init_attribute()

        # 初始化获取的参数
        self._request = request
        self._size = size
        self._page = page

        # 计算page_start和page_end
        self._set_page_start_and_end()

    def _init_attribute(self):
        self.page_start = 0
        self.page_end = 0
        self.error_msg = None

    def _set_page_start_and_end(self):
        """
        计算page_start和page_end
        :return:
        """

        if self._request is not None:
            # 确保传入的request是正确的request请求类型，且通过get方式传递过来的page和size均为int类型
            self._get_page_size_from_request()
        elif self._page is not None and self._size is not None:
            # 确保传入的page和size均为有效的int类型数据
            if not self._check_int_page_and_size():
                self.error_msg = "传入了错误类型的page: %s和size: %s" % (self._page, self._size)
        else:
            self.error_msg = "未传入有效的request或page和size"

        if self.error_msg is None:
            self._calculate_page_start_and_end()

    def _calculate_page_start_and_end(self):
        # 根据page_no和page_size获取分页信息

        # 获取开始和结束位置
        try:
            self.page_start = (self._page - 1) * self._size
            self.page_end = self._page * self._size

            if self.page_start < 0:
                self.page_start = 0
            if self.page_end < 0:
                self.page_end = 0
        except Exception as e:
            self.error_msg = e

    def _get_page_size_from_request(self):
        # 从request中获取page和size

        if isinstance(self._request, WSGIRequest):
            # 从request的get中获取page和size
            page = self._request.GET.get("page")
            size = self._request.GET.get("size")

            if page is not None or size is not None:
                self._page = page
                self._size = size

                if not self._check_int_page_and_size():
                    self.error_msg = "request中传递了错误类型的page：%s 和size： %s" % (self._page, self._size)
            else:
                # 当request的get中未传入page和size时，使用默认的page和size
                if not self._check_int_page_and_size():
                    self.error_msg = "传入了错误的page: %s 和size: %s" % (self._page, self._size)
        else:
            self.error_msg = "传入的request是错误的类型： %s" % type(self._request)

    def _check_int_page_and_size(self):
        # 检验self中的_page和_size是否是int类型的数据

        check = False

        try:
            self._page = int(self._page)
            self._size = int(self._size)
            check = True
        except Exception as e:
            del e

        return check
