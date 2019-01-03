#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/6/6 11:28
# @Author  : Zhanhui
# @File    : my_es.py


from elasticsearch import Elasticsearch, RequestsHttpConnection


def es_connection_server(server_ip, port=9200, proxy=None, timeout=60, max_retries=10, retry_on_timeout=True):
    # 初始化es连接服务

    class MyConnection(RequestsHttpConnection):
        def __init__(self, *args, **kwargs):
            proxies = kwargs.pop('proxies', {})
            super(MyConnection, self).__init__(*args, **kwargs)
            self.session.proxies = proxies

    url = "%s:%s" % (server_ip, port)

    # 初始化连接参数
    connection_params = {
        "connection_class": MyConnection,
        "timeout": timeout,
        "max_retries": max_retries,
        "retry_on_timeout": retry_on_timeout,
    }
    if proxy is not None:
        connection_params["proxies"] = {"http": proxy}

    es_client = Elasticsearch([url], **connection_params)

    return es_client
