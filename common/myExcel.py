# -*- coding: utf-8 -*-
import json
import os
import xlwt
import xlrd
from xlutils.copy import copy
from common.myLogger import logger


class Excel(object):
    def __init__(self):
        self.file_path = None

    def set_style(self, name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font

    def read_excel(self, file_name):
        if isinstance(file_name, str):  # 判断是否是字符串类型
            if file_name.endswith('.xls'):  # 判断字符串以什么结尾
                self.file_path = os.path.dirname(os.path.dirname(__file__)) + '/dataFile/{}'.format(file_name)
                workbook = xlrd.open_workbook(self.file_path)  # 打开一个workbook
                # 抓取所有sheet页的名称
                worksheets = workbook.sheet_names()
                for worksheet_name in worksheets:
                    worksheet = workbook.sheet_by_name(worksheet_name)
                    # 遍历sheet1中所有行row
                    num_rows = worksheet.nrows  # 获取sheet行数
                    row_demo = ['用例集编号', '用例标识', '模块名称', '接口名称', '用例描述', '请求url', '请求方式',
                                '请求头部', '用例说明', '前置处理',  '请求数据', '匹配规则', '预期结果', '后置处理',
                                '优先级', '是否执行','被依赖value', '响应数据', '状态码', '执行结果', '执行时间',
                                '备注']
                    # 判断模板第二行格式
                    # print(worksheet.row_values(1))
                    if worksheet.row_values(1)[0:22] == row_demo:  # 判断sheet1表头是否与预期模板一致
                        all_row_value = []
                        for curr_row in range(num_rows-2):  # 获取表格三行以后数据，包括第三行
                            row_value = worksheet.row_values(curr_row + 2)
                            all_row_value.append(row_value[0:17])  # 将表格0-16列数据转化为列表
                        logger.debug("{}".format(worksheet.row_values(1)))  # 表头
                        logger.debug("{}".format(all_row_value))  # 表格0-16列数据
                        return all_row_value  # 返回第三列后的所有数据
                    else:
                        logger.error("用例模板表头格式有误")
                        exit(0)
                        # return "用例模板格式有误"
            else:
                logger.error("读取的不是.xls文件")
                exit(0)
        else:
            logger.error("用例文件格式有误")
            exit(0)

    def xlutils_excel(self, row_value, col_value, value, info=None):
        rb = xlrd.open_workbook(self.file_path, formatting_info=True)  # formatting_info 带格式导入
        wb = copy(rb)  # 利用xlutils.copy下的copy函数复制
        ws = wb.get_sheet(0)  # 获取表单0
        rs = rb.sheet_by_index(0)
        # ws.write(0, 0, 'changed!')  # 改变（0,0）的值
        value_row_col = rs.cell(row_value, col_value).value  # 表格原有值
        if not value:
            ws.write(row_value, col_value, value)

        else:
            if not value_row_col :
                ws.write(row_value, col_value, value)  # 增加指定列的值
            else:
                ws.write(row_value, col_value, "{}；{}".format(value_row_col, value))  # 增加指定列的值
        if info:
            logger.debug("{}:({}, {}, {})".format(info, row_value, col_value, value))
        else:
            logger.debug((row_value, col_value, value))
        try:
            wb.save(self.file_path)  # 保存文件
        except Exception as msg:
            logger.error("保存excel文件失败:{}".format(msg))


my_excel = Excel()


