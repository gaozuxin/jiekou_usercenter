# -*- coding: utf-8 -*-
import json
import re
import time

import requests
from common.formatTime import date_time_chinese
from common.headerSign import sign
from common.myLogger import logger


class Requests(object):
    def __init__(self):
        pass

    def is_json(self, data):
        try:
            data = eval(data.replace('null', 'None'))  # 处理json种的NULL
            return data
        except:
            return False

    def request_post(self, url, data):
        timestampt = int(time.time() * 1000)
        data_dict = {
            "accountNo": "T9-TServer",
            "secretCode": "fbw77t42dlb3cw6z",
            "timestamp": timestampt}
        data_dict["data"] = data
        authentication = sign.get_authentication(None, data_dict)
        header_dict = {
            "Content-Type": "application/json",
            "requestId": "1",
            "timestamp": str(timestampt),
            "authentication": authentication
        }
        # print(header_dict)
        logger.debug("请求url:{};请求头:{};请求数据:{}".format(url, header_dict, data))
        res = requests.post(url=url, headers=header_dict, json=data)  # 发送请求
        # data_eval = json.loads(r.text)  # 字符串转成字典类型
        # print(data_eval)
        return res

    def request_get(self, url, data):
        timestampt = int(time.time() * 1000)
        # is_true = self.is_json(data)
        # print(is_true)
        # if isinstance(is_true, dict):
        #     data = is_true
        # else:
        #     url = "{}/{}".format(url, data)
        #     data = None
        data_dict = {
            "accountNo": "T9-TServer",
            "secretCode": "fbw77t42dlb3cw6z",
            "timestamp": timestampt
        }
        data_dict["data"] = data
        authentication = sign.get_authentication(None, data_dict)
        print(authentication)
        header_dict = {
            "requestId": "1",
            "timestamp": str(timestampt),
            "authentication": authentication
        }
        logger.debug("请求url:{};请求头:{};请求数据:{}".format(url, header_dict, data))
        res = requests.get(url=url, headers=header_dict, params=data)
        return res


class RunMethod(object):
    def __init__(self):
        logger.info("-" * 32 + date_time_chinese() + "-" * 32)

    def post_main(self, url, data, header=None):
        if header != None:
            res = requests.post(url=url, data=json.loads(data), headers=json.loads(header))
        else:
            res = requests.post(url=url, data=data)
        return res

    def get_main(self, url, data=None, header=None):
        if header != None:
            res = requests.get(url=url, data=data, headers=header, verify=False)
        else:
            res = requests.get(url=url, data=data, verify=False)
        return res

    def run_main(self, method, url, data=None, header=None):
        if method == 'POST':
            res = self.post_main(url, data, header)
        elif method == 'GET':
            res = self.get_main(url, data, header)
        else:
            res = None
        return res
        # return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)


req = Requests()
