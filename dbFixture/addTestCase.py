# -*- coding: utf-8 -*-
from common.formatTime import date_time
from common.myExcel import my_excel

from common.myMysql import mysql


file_name = "case_template.xls"
all_value = my_excel.read_excel(file_name)  # 表格中三行以后的数据


sql = "INSERT INTO test_case (suite_number,case_number,module,name,description,url,method,headers,depend_key,data," \
      "rule,expect_result,priority,is_execute,depend_value,create_time) values "
for index in range(len(all_value)):
    if index == 0:
        sql = "{}({},'{}')".format(sql, str(all_value[index][0:15]).strip("[").strip("]"), date_time())
    else:
        sql = "{},({},'{}')".format(sql, str(all_value[index][0:15]).strip("[").strip("]"), date_time())
print(sql)
mysql.update(sql)
