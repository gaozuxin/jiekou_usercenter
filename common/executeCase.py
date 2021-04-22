# -*- coding: utf-8 -*-
import os
import re
from common.myExcel import my_excel
from common.myLogger import logger
from common.formatTime import date_time, date_time_chinese
from common.myMysql import mysql
from common.myRedis import my_redis
from common.myRequest import req
from common.readConfig import read_config


class ExecuteCaseExcel(object):
    def __init__(self):
        logger.info("-" * 32 + date_time_chinese() + "-" * 32)
        cfg = read_config(os.path.dirname(os.path.dirname(__file__)) + '/cfg/config.ini')
        self.base_url = cfg.get('base_para', 'base_url')
        self.file_name = cfg.get('base_para', 'file_name')
        self.mysql_status = cfg.get("base_para", "mysql_status")
        self.redis_status = cfg.get("base_para", "redis_status")
        self.suite_num = None
        self.depend_dict = {}

    def case_process(self, process_data, col_num):  # 前置处理、后置处理执行，校验
        try:
            process_data = eval(process_data)
            process_type = ["mysql", "redis"]  # 支持校验的类型
            no_type = set(process_data.keys()).difference(set(process_type))  # 不支持校验的类型
            if len(no_type) > 0:  # 不支持类型大于0，类型写入日志
                logger.error('预置处理类型{}暂不支持'.format(no_type))
            if self.mysql_status == "1" and "mysql" in process_data and process_data["mysql"] is not None:
                for sql_data in process_data["mysql"]:
                    if len(sql_data) == 2:  # 判断sql列表子元素的长度，==2 执行且校验
                        if "select" in sql_data[0].lower():
                            sql_res = mysql.select_all(sql_data[0])
                            if str(sql_res) == sql_data[1]:
                                pass
                            else:
                                my_excel.xlutils_excel(col_num + 2, 22,
                                                       'SQl语句处理验证失败：语句：{} 期望:{} 实际值:{}'.format(
                                                           sql_data, sql_data[1], sql_res))
                                logger.error('SQl语句处理验证失败：语句：{} 期望:{} 实际值:{}'.format(
                                    sql_data, sql_data[1], sql_res))
                        elif "update" in sql_data[0].lower() or "delete" in sql_data[0].lower() \
                                or "insert" in sql_data[0].lower():
                            sql_res = mysql.update(sql_data[0])
                            if str(sql_res) == sql_data[1]:
                                pass
                            else:
                                logger.error('SQl语句处理验证失败：语句：{} 期望:{} 实际值:{}'.format(
                                    sql_data, sql_data[1], sql_res))
                                my_excel.xlutils_excel(col_num + 2, 22,
                                                       'SQl语句处理验证失败：语句：{} 期望:{} 实际值:{}'.format(
                                                           sql_data, sql_data[1], sql_res))
                        else:
                            logger.error('非select的SQL的语句，需有校验项，异常SQL语句【{}】'.format(sql_data))

                    elif len(sql_data) == 1:  # ==1 只执行不校验
                        if "select" in sql_data[0].lower():
                            mysql.select_all(sql_data[0])
                        elif "update" in sql_data[0].lower() or "delete" in sql_data[0].lower() \
                                or "insert" in sql_data[0].lower():
                            mysql.update(sql_data[0])
                        else:
                            logger.error("SQL语句格式异常，异常SQL语句【{}】".format(sql_data))
                            my_excel.xlutils_excel(col_num + 2, 22,
                                                   "SQL语句格式异常，异常SQL语句【{}】".format(sql_data))

                    elif len(sql_data) > 2:
                        logger.error("SQL语句格式异常，异常SQL语句【{}】".format(sql_data))
                        my_excel.xlutils_excel(col_num + 2, 22,
                                               "SQL语句格式异常，异常SQL语句【{}】".format(sql_data))
            if self.redis_status == "1" and "redis" in process_data and process_data["redis"] is not None:  # redis语句处理
                for redis_data in process_data["redis"]:
                    if len(redis_data) == 2:  # 判断redis列表子元素的长度，==2 执行且校验
                        redis_res = my_redis.del_redis(redis_data[0])
                        if redis_res == redis_data[1]:
                            pass
                        else:
                            logger.error('redis语句处理验证失败：语句：{} 期望:{} 实际值:{}'.format(
                                                       redis_data, redis_data[1], redis_res))
                            my_excel.xlutils_excel(col_num + 2, 22,
                                                   'redis语句处理验证失败：语句：{} 期望:{} 实际值:{}'.format(
                                                       redis_data, redis_data[1], redis_res))
                            pass
                    elif len(redis_data) == 1:  # ==1 只执行不校验
                        my_redis.del_redis(redis_data[0])
                    elif len(redis_data) > 2:
                        logger.error("redis语句格式异常，异常redis语句【{}】".format(redis_data))
            else:
                pass
        except Exception as msg:
            logger.error("处理数据解析异常:{} ".format(msg))

    def get_case(self):
        all_data = my_excel.read_excel(self.file_name)
        return all_data

    def exe_case(self, suite_number, case_number, url, method, data, rule, expect_result, depend_value, col_num,
                 front_process, rear_process):
        if url.startswith('/'):  # 请求url是否以‘/’开头，前面加上域名
            url = self.base_url + url  # 请求url
        else:
            pass
        if self.suite_num == suite_number:  # 与上条用例是否同一用例集
            logger.info("---------------[{}]用例开始执行---------------".format(case_number))
        else:
            """
            如果不是同一用例集：
            1.清空用例依赖字典数据；
            2.更新用例集编号
            """
            logger.info("-" * 35 + "【{}】用例集".format(suite_number) + "-" * 35)
            logger.info("---------------[{}]用例开始执行---------------".format(case_number))
            self.depend_dict = {}  # 依赖字典设置为空
            self.suite_num = suite_number  # 用例集设置为新用例集
        depend_dict = self.depend_dict  # 用例依赖，depend_dict变量data入参使用
        if data:
            try:
                data = eval(data.replace('null', 'None'))  # 处理json种的NULL
            except Exception as msg:
                logger.error("请求数据解析异常:{}".format(msg))
        if front_process:
            self.case_process(front_process, col_num)  # 执行前置处理
        if method.upper() == "POST":
            res = req.request_post(url, data)
        elif method.upper() == "GET":
            res = req.request_get(url, data)
        if rear_process:
            self.case_process(rear_process, col_num)  # 执行后置处理
        # res_data = json.loads(res.text)
        res_text = res.text
        res_data = res.json()  # 下面代码种数据类型强转使用
        res_code = res.status_code
        if depend_value:  # 存在被依赖value,放入字典
            depend_lists = re.split('[，,]', depend_value.strip())  # 被依赖value,获取数据去除首尾空格；以，或,切割数据
            for depend_list in depend_lists:  # 遍历被依赖value,例：uuid=$["data"]["uuid"]
                values = re.split('==|=', depend_list)
                try:
                    value = values[1].strip().strip('“|"|‘').strip("'|”|’")  # 例：$["data"]["uuid"]
                    key = values[0].strip()  # 例：uuid
                    if value[0] == '$':
                        data_rep = value.replace('$', 'res_data')  # 替换后的变量是字符串类型,如：data_rep = res_data["_msg"]
                        # 将字符串转成取字典值比对 ，用到了前面的变量res_data, 出现异常时，本用例集下的测试用例不应该再运行
                        self.depend_dict[key] = eval(data_rep)
                    else:
                        logger.error('被依赖value格式需如:uuid=$["data"]["uuid"] 当前:{}'.format(values))
                except Exception as msg:
                    logger.error("用例依赖处理异常{},被依赖value【{}】".format(msg, values))
                    # raise("用例依赖处理异常{},{}".format(values, msg))
        else:
            pass

        # 后置处理
        my_excel.xlutils_excel(col_num + 2, 17, "{}".format(res_text), "用例服务器响应数据")  # 写入响应数据
        my_excel.xlutils_excel(col_num + 2, 18, "{}".format(res_code), "服务器返回状态码")  # 写入实际结果
        my_excel.xlutils_excel(col_num + 2, 20, date_time(), "用例执行时间")  # 写入执行时间
        flag = -1
        if expect_result:
            if rule == "包括":
                flag = expect_result in res_text
                if flag == 1:
                    pass
                else:
                    my_excel.xlutils_excel(col_num + 2, 21,
                                           '验证失败：匹配规则【{}】 期望:{} 实际值:{}'.format(rule, expect_result, res_text))
                    logger.info('验证失败：匹配规则【{}】 期望:{} 实际值:{}'.format(rule, expect_result, res_text))
            elif rule == "相等":
                if res_text == expect_result:
                    flag = 1
                else:
                    flag = 0
                    my_excel.xlutils_excel(col_num + 2, 21,
                                           '验证失败：匹配规则【{}】 期望:{} 实际值:{}'.format(rule, expect_result, res_text))
                    logger.info('验证失败：匹配规则【{}】 期望:{} 实际值:{}'.format(rule, expect_result, res_text))
            elif rule == "匹配":
                try:
                    expected_res = re.split('[，,]', expect_result.strip())  # 预期结果,表格数据去除首尾空格；以，或,切割数据
                    # res_data = json.loads(res_data)  # 实际结果字符串转成json串，这个变量是有用的，不注释掉
                    for exp_res in expected_res:  # 遍历预期结果
                        values1 = re.split('==|=', exp_res)
                        value1 = values1[1].strip().strip('“|"|‘').strip("'|”|’")
                        key1 = values1[0].strip()
                        if key1[0] == '$':
                            data_rep = key1.replace('$', 'res_data')  # 替换后的变量是字符串类型,如：data_rep = res_data["_msg"]
                            actual_value = eval(data_rep)  # 将字符串转成取字典值比对 ，用到了前面的变量res_data
                            if str(actual_value) == str(value1):  # 执行结果与期望数据比较
                                flag = 1
                            else:
                                flag = 0
                                my_excel.xlutils_excel(col_num + 2, 21,
                                                       '【{}】用例验证失败：匹配规则【{}】 期望:{} 实际值:{}={}'.format(
                                                           case_number, rule, exp_res, data_rep, actual_value))
                                logger.error('【{}】用例验证失败：匹配规则【{}】 期望:{} 实际值:{}={}'.format(
                                    case_number, rule, exp_res, data_rep, actual_value))
                                break
                        else:
                            my_excel.xlutils_excel(col_num + 2, 21,
                                                   '当匹配规则是[匹配]时，预期结果格式需如:$["code"] = "000000" 当前:{}'.format(exp_res))
                            # logger.error('当匹配规则是[匹配]时，预期结果格式需如:$["code"] = "000000" 当前:{}'.format(exp_res))
                            flag = -1
                            break
                except Exception as msg:
                    my_excel.xlutils_excel(col_num + 2, 21,
                                           '预期结果处理异常:{} 期望:{}'.format(msg, expect_result), "预期结果解析异常")
                    flag = -1
            elif rule == "正则":
                try:
                    re_data = re.search(expect_result, res_text)
                    if re_data is None:
                        flag = 0
                        my_excel.xlutils_excel(col_num + 2, 21,
                                               '【{}】用例验证失败：匹配规则【{}】 期望:{} 实际值:{}'.format(
                                                   case_number, rule, expect_result, res_text))
                    else:
                        flag = 1
                except Exception as msg:
                    my_excel.xlutils_excel(col_num + 2, 21,
                                           '正则匹配结果处理异常:{} 期望:{}'.format(msg, expect_result), "正则匹配结果处理异常")
                    flag = -1
            else:
                my_excel.xlutils_excel(col_num + 2, 21,
                                       '【{}】用例验证失败原因：匹配规则【{}】暂不支持'.format(case_number, rule))
                logger.error('【{}】用例验证失败原因：匹配规则【{}】暂不支持'.format(case_number, rule))
                flag = -1
        elif res_code == 200:  # 预期结果为空，且状态码为200
            flag = 1
        else:
            pass  # 预期结果为空，且状态码不为200，认为异常
        if flag == 1:
            my_excel.xlutils_excel(col_num + 2, 19, '通过', "用例执行结果")  # 写入执行结果
            logger.info("【{}】用例执行通过".format(case_number))
        elif flag == 0:
            my_excel.xlutils_excel(col_num + 2, 19, '未通过', "用例执行结果")
            logger.info("【{}】用例执行未通过".format(case_number))
            assert flag == 1  # flag = 0(未通过)
        else:
            my_excel.xlutils_excel(col_num + 2, 19, '异常', "用例执行结果")
            logger.error("【{}】用例执行异常".format(case_number))
            assert flag == 1  # flag = -1(异常)


exe = ExecuteCaseExcel()
# if __name__ == '__main__':
#     all_case = exe.get_case()
#     print(all_case)
