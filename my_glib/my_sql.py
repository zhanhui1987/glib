#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/3/15 14:43
# @Author  : Zhanhui
# @File    : my_sql.py


import logging
import pymysql
import time


class Connection(object):
    def __init__(self, host, database, user=None, password=None,
                 max_idle_time=7*3600, auto_commit=True, print_query=False):
        self._db = None
        self._print_query = print_query

        # 设置数据库连接的最长时间
        self._max_idle_time = max_idle_time

        # 获取最后一次连接数据库的时候
        self._last_use_time = time.time()

        # 是否自动commit
        self._auto_commit = auto_commit

        # 设置连接数据库时需要用到的各种参数
        self._db_args = {
            'use_unicode': True,
            'charset': "utf8mb4",
            'db': database,
            'init_command': 'SET time_zone = "+8:00"',
            'sql_mode': "TRADITIONAL"
        }
        if user is not None:
            self._db_args["user"] = user
        if password is not None:
            self._db_args["passwd"] = password

        # 设置host和port
        pair = host.split(":")
        if len(pair) == 2:
            self._db_args["host"] = pair[0]
            self._db_args["port"] = int(pair[1])
        else:
            self._db_args["host"] = host
            self._db_args["port"] = 3306

        self._reconnect()

        # 定义类的初始值
        self._query_data = []
        self.last_row_id = 0
        self.row_count = 0

    def __del__(self):
        # 在类结束后，应关闭与mysql的连接

        self._close()

    def _close(self):
        # 关闭mysql的连接
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def _reconnect(self):
        # 关闭已经创建的数据库连接，再重新连接

        self._close()
        try:
            self._db = pymysql.connect(**self._db_args)
            self._db.autocommit(self._auto_commit)
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self._db_args["host"], exc_info=True)
            raise

    def _cursor(self):
        # 获取数据库连接的游标

        # 若数据库连接的空闲时间超过最大连接的时间，则将其重新连接。
        # Mysql默认最大的空闲时间是8小时。
        idle_time = time.time() - self._last_use_time
        if self._db is None or idle_time > self._max_idle_time:
            self._reconnect()
        self._last_use_time = time.time()

        # 将游标返回的值设置为dict结构
        try:
            return self._db.cursor(cursor=pymysql.cursors.DictCursor)
        except pymysql.OperationalError:
            raise

    def _init_execute(self):
        # 在每次执行新的query语句时，需要将类的一些属性进行初始化

        self._init_query_data()
        self.last_row_id = 0
        self.row_count = 0

    def _init_query_data(self):
        # 将类的 _query_data 属性进行初始化

        self._query_data = []

    def execute(self, query, print_query=False):
        # 执行query语句，返回语句影响到的数据总数

        # 根据传入的参数，判断是否需要输出query语句
        if self._print_query or print_query:
            print("QUERY： %s" % query)

        # 初始化查询结果
        self._init_execute()

        cursor = self._cursor()

        success = False

        try:
            cursor.execute(query)
            self._query_data = cursor.fetchall()
            if not self._query_data:
                self._query_data = []

            self.row_count = cursor.rowcount
            # 尝试获取query执行后最后一个插入的自增id，并将其赋给类的属性：last_row_id
            try:
                self.last_row_id = cursor.lastrowid
                if self.last_row_id is None:
                    self.last_row_id = 0
            finally:
                pass

            # 若query语句受影响的行数为0，则默认该query未生效，否则认为其生效。
            if self.row_count > 0:
                success = True
        except Exception as e:
            print(e)
            print("ERROR QUERY： %s" % query)
        finally:
            # 执行结束之后，要把cursor关闭
            cursor.close()

        return success

    @property
    # 将类的函数转换成类的属性
    def data(self):
        # 返回查询的所有结果，并将结果初始化

        res_data = self._query_data
        self._init_query_data()

        return res_data

    @property
    # 返回count总数，若query查询的是count(*)的话
    def count(self):
        count = 0

        res_data = self._query_data
        if isinstance(res_data, list) and res_data:
            for row in res_data:
                if len(row.keys()) == 1 and "count(*)" in row.keys():
                    count = row["count(*)"]

                    break

        self._init_query_data()

        return count


def q(origin_str):
    #  escape字符串，并在其首尾添加单引号，用于拼接mysql query语句

    if origin_str is None:
        origin_str = ''
    return "'{}'".format(pymysql.escape_string(str(origin_str)))


def main():
    con = Connection(host='127.0.0.1', database='test', user='test_user', password='test_password')
    #    query = "show tables like %s" % q('%test%')
    query = "show tables"

    if con.execute(query):
        print("query 执行成功")

        print("query 影响的行数： %s" % con.row_count)
        print("query 最后一个插入的自增ID： %s" % con.last_row_id)
        print("query 的返回结果: %s" % con.data)
        print("query 的返回结果只能获取一次，再次取时: %s" % con.data)
    else:
        print("query 执行失败！")


if __name__ == "__main__":
    main()
