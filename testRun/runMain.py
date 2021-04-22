# -*- coding: utf-8 -*-
import os
import sys
# current_path = os.path.dirname(os.path.dirname(__file__))
# sys.path.append(current_path)
import unittest
from BeautifulReport import BeautifulReport
from common.executeCase import exe
from common.formatTime import date_time
from common.myExcel import my_excel
from common.myLogger import logger
SkipCount = 0


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDown(cls):
        pass

    def action(self, *all_data):
        suite_number = all_data[0][0]  # 用例集编号
        case_number = all_data[0][1]  # 用例标识
        url = all_data[0][5]  # 请求url
        method = all_data[0][6]  # 请求方式
        # headers = all_data[0][7]  # 请求头部
        front_process = all_data[0][9]  # 前置处理
        data = all_data[0][10]  # 请求数据
        rule = all_data[0][11]   # 匹配规则
        expect_result = all_data[0][12]  # 预期结果
        rear_process = all_data[0][13]  # 后置处理
        is_execute = all_data[0][15]  # 是否执行
        depend_value = all_data[0][16]  # 被依赖value
        col_num = all_data[1]
        if is_execute.upper() == 'Y':
            exe.exe_case(suite_number, case_number, url, method, data, rule, expect_result, depend_value, col_num,
                         front_process, rear_process)
        else:  # 用例执行否
            logger.info("---------------[{}]用例开始执行---------------".format(case_number))
            my_excel.xlutils_excel(col_num + 2, 20, date_time(), "用例执行时间")  # 写入执行时间
            my_excel.xlutils_excel(col_num + 2, 19, '跳过', "用例执行结果")
            logger.info("【{}】用例跳过".format(case_number))
            global SkipCount
            SkipCount += 1

    @staticmethod
    def getTestFunc(*args):
        def func(self):
            self.action(*args)
        func.__doc__ = args[0][4]  # 修改用例描述
        return func


def generateTestCases(arglists):  # 动态生成测试用例
    global case_names
    for index in range(len(arglists)):
        args = arglists[index]
        case_names.append(args[1])
        setattr(MyTestCase, args[1], MyTestCase.getTestFunc(args, index))


def _main():
    all_data = exe.get_case()  # 获取表格测试用例
    for col_num in range(len(all_data)):  # 遍历测试用例
        for index in range(17, 23):  # 文件初始化
            my_excel.xlutils_excel(col_num + 2, index, "", "excel文件初始化")
    generateTestCases(all_data)  # 动态生成测试用例函数


if __name__ == '__main__':
    case_names = []
    _main()  # 动态生成测试用例
    suite = unittest.TestSuite()  # 定义一个用例集合
    for case_name in case_names:
        suite.addTest(MyTestCase(case_name))  # 测试用例添加到用例集合
    testdir = os.path.dirname(os.path.dirname(__file__))
    test_dir = os.path.join(testdir, 'testCase')  # 测试用例文件夹
    report_dir = os.path.join(testdir, 'result/report')
    # now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
    # filename = '用户中心接口测试报告' + str(now)
    filename = '用户中心接口测试报告'
    rep = BeautifulReport(suite)
    rep_count = rep.stopTestRun(SkipCount)  # 获取测试结果
    rep.report(description='用户中心测试', filename=filename, report_dir=report_dir)
    rep_num = {
        'all': rep_count['testAll'],
        'pass': rep_count['testPass'] - SkipCount,
        'fail': rep_count['testFail'],
        'skip': SkipCount
    }
    print(rep_num)
    if rep_num['fail'] == 0:
        print("测试用例全部通过")
    else:
        print("测试未通过，请分析测试结果")
    print("代码更新测试")
