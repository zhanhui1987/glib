#!/usr/bin/env python3
# coding: utf-8

# @Time    : 2018/2/10 12:52
# @Author  : Zhanhui
# @File    : my_excel.py


import os
import xlrd
import xlwt


class ExcelRead(object):
    # 初始化Excel对象
    def __init__(self, file_name, header_map=None):
        self._file_name = os.path.realpath(file_name)
        self._header_map = header_map
        self._data = None

    # 读取Excel中的内容
    def _read_excel(self):
        try:
            self._data = xlrd.open_workbook(self._file_name)
        except Exception as e:
            print(e)

    # 获取Excel的sheet列表
    def _get_sheet(self):
        self._read_excel()
        if self._data is not None and isinstance(self._data, xlrd.book.Book):
            self._sheets = [sheet.name for sheet in self._data.sheets()]
        else:
            self._sheets = []

    # 返回Excel的sheet列表
    def get_sheets(self):
        self._get_sheet()
        return self._sheets

    def read(self, has_header=True, header_map=None, max_row=0):
        # 通过Excel的name来获取每一个sheet的内容。max_row用于设置最多读取的行数，不包括表头。

        excel_data = []
        sheets = self.get_sheets()
        for sheet in sheets:
            data_dict = {
                'sheet_name': sheet,
                'sheet_data': [],
                'sheet_header': [],
            }

            table = self._data.sheet_by_name(sheet)
            sheet_data_list, sheet_header_list = self._parse_table(table, has_header, header_map, max_row)

            data_dict["sheet_data"].extend(sheet_data_list)
            data_dict["sheet_header"].extend(sheet_header_list)
            excel_data.append(data_dict)

        return excel_data

    @staticmethod
    def _parse_table(table, has_header=True, header_map=None, max_num=0):
        sheet_data_list = []
        sheet_header_list = []
        if table is not None and isinstance(table, xlrd.sheet.Sheet):
            n_rows = table.nrows
            n_cols = table.ncols

            # 若Excel有表头，则需要获取该表头；否则使用从0开始的列数作为表头
            if has_header is True:
                sheet_header_list = table.row_values(0)
                if max_num > 0:
                    max_num += 1
            else:
                sheet_header_list = [n for n in range(n_cols)]

            # 循环每一行，将每一行的数据转换成以表头为键，内容为值的字典，保存到数据数组中
            for row_num in range(n_rows):
                if row_num >= max_num > 0:
                    break

                # 若Excel有表头，则第一行不进行处理
                if has_header is True and row_num == 0:
                    continue

                # 将每一行的内容进行转换
                row = table.row_values(row_num)
                if isinstance(row, list):
                    res_row = {}
                    for col_num in range(n_cols):
                        res_row_key = sheet_header_list[col_num]
                        # 如果传入了表头的替换对应关系，需要将表头进行替换
                        if isinstance(header_map, dict) and sheet_header_list[col_num] in header_map.keys():
                            res_row_key = header_map[sheet_header_list[col_num]]
                        res_row[res_row_key] = row[col_num]

                    sheet_data_list.append(res_row)

        return sheet_data_list, sheet_header_list


class ExcelWrite(object):
    def __init__(self, file_name, sheet_max_row=60000):
        self._file_name = os.path.realpath(file_name)
        self._sheet_max_row = sheet_max_row  # _sheet_max_row用来设置每个sheet中包含的最大行数

    def write(self, data, data_only=False, headers=None, header_map=None):
        # data_only表示data中只包含有需要保存到Excel中的数据，没有name和header等信息
        if data_only is True:
            if isinstance(headers, list):
                save_data = self._parse_data(data, headers)
            else:
                save_data = []
                print("需要传入Excel文件的表头列表！")
        else:
            save_data = self._split_data(data)

        try:
            self._write_save_data(save_data, header_map)
        except Exception as e:
            print(e)

    def _split_data(self, data):
        # 需要确保每个sheet中的数据总数都不超过self._sheet_max_row
        save_data = []

        for sub_data in data:
            name = sub_data.get("sheet_name")
            data = sub_data.get("sheet_data")
            header = sub_data.get("sheet_header")

            if self._check_data_type(name, data, header):
                # 查看data的长度是否超过self._sheet_max_row，超过的话，需要对其进行拆分
                data_len = len(data)
                if data_len > self._sheet_max_row:
                    sheet_count = data_len // self._sheet_max_row
                    if data_len % self._sheet_max_row:
                        sheet_count += 1

                    # 确保每个sheet的数字后缀长度是一致的
                    sheet_count_len = len(str(sheet_count))
                    if sheet_count_len < 3:
                        sheet_count_len = 3

                    for i in range(sheet_count):
                        # 拆分data
                        sub_save_data_start = i * self._sheet_max_row
                        sub_save_data_end = (i + 1) * self._sheet_max_row - 1

                        # 确保sub_save_data结束的索引不大于data的长度
                        if sub_save_data_end > data_len - 1:
                            sub_save_data_end = data_len

                        sub_save_data = {
                            r"sheet_name": "%s%0*s" % (name, sheet_count_len, (i + 1)),
                            r"sheet_data": data[sub_save_data_start:sub_save_data_end],
                            r"sheet_header": header,
                        }

                        save_data.append(sub_save_data)
                else:
                    save_data.append(sub_data)

        return save_data

    def _parse_data(self, data, headers):
        # 将data_only的数据处理成指定的数据结构，并对其进行数据拆分处理
        save_data = [
            {
                r'sheet_name': 'Sheet',
                r'sheet_data': data,
                r'sheet_header': headers,
            }
        ]

        return self._split_data(save_data)

    def _write_save_data(self, save_data, header_map):
        # 将之前处理好的数据写入到Excel中

        if isinstance(save_data, list) and save_data:
            xls = xlwt.Workbook(encoding='utf-8')
            header_row = 0

            for sub_data in save_data:
                name = sub_data.get("sheet_name")
                data = sub_data.get("sheet_data")
                header = sub_data.get("sheet_header")
                col_count = len(header)

                if self._check_data_type(name, data, header):
                    sheet = xls.add_sheet(name, cell_overwrite_ok=True)

                    # 写入header
                    for col_num in range(col_count):
                        header_name = header[col_num]

                        if isinstance(header_map, dict) and header_name in header_map.keys():
                            sheet.write(header_row, col_num, header_map[header_name])
                        else:
                            sheet.write(header_row, col_num, header_name)

                    # 写入row，上下线均+1是因第一行用来写header
                    for row_num in range(1, len(data) + 1):
                        row = data[row_num - 1]
                        for col_num in range(col_count):
                            header_name = header[col_num]
                            sheet.write(row_num, col_num, row[header_name])

            xls.save(self._file_name)
        else:
            print("无法获取写入Excel的数据列表！")

    @staticmethod
    def _check_data_type(name, data, header):
        # 检测需要保存的各个数据类型是否是正确的

        errors = []

        if name is None:
            errors.append("sheet name is %s" % name)
        if not isinstance(data, list):
            errors.append("sheet data is not a list")
        if not isinstance(header, list):
            errors.append("sheet header is not a list")

        if errors:
            print("ERROR : " + ", ".join(errors))
            return False
        else:
            return True


def main():
    excel_file = r"test.xlsx"

    er = ExcelRead(excel_file)
    sheets = er.get_sheets()
    print(sheets)

    data = er.read(max_row=100)
#    print(data)

    for sub_data in data:
        print(sub_data.get("sheet_name"))
        print(sub_data.get("sheet_header"))

        rows = sub_data.get("sheet_data")
        headers = sub_data.get("sheet_header")

        for row in rows:
            for header in headers:
                print("%s : %s" % (header, row.get(header)))
            break

        break


if __name__ == "__main__":
    main()
