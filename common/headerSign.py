# -*- coding: utf-8 -*-
import hashlib


class Sign(object):
    def __init__(self):
        self.param_array = []

    def to_list(self, auth_key, data):
        if isinstance(data, list):
            for index in range(len(data)):
                if isinstance(data[index], list):
                    self.to_list(auth_key, data[index])
                elif isinstance(data[index], dict):
                    self.to_list(None, data[index])
                else:
                    if data[index] is None:
                        pass
                    else:
                        self.param_array.append("{}={}".format(auth_key, data[index]))

        elif isinstance(data, dict):
            for key in data:
                if isinstance(data[key], dict):
                    self.to_list(None, data[key])
                elif isinstance(data[key], list):
                    self.to_list(key, data[key])
                else:
                    if data[key] is None:  # 空为真
                        pass
                    else:
                        self.param_array.append("{}={}".format(key, data[key]))
        else:
            print("签名参数异常")

    def get_authentication(self, auth_key, data):
        self.param_array = []
        self.to_list(auth_key, data)
        new_param = "&".join(sorted(self.param_array))
        print(new_param)  # 加密前字符串
        authentication = hashlib.md5(new_param.encode(encoding='UTF-8')).hexdigest().upper()
        return authentication


sign = Sign()
# param_array = []
# def get_authentication(auth_key, data):
#
#     def to_list(auth_key, data):
#
#         global param_array
#         if isinstance(data, list):
#             for index in range(len(data)):
#                 if isinstance(data[index], list):
#                     to_list(auth_key, data[index])
#                 elif isinstance(data[index], dict):
#                     to_list(None, data[index])
#                 else:
#                     if data[index] is None:
#                         pass
#                     else:
#                         param_array.append("{}={}".format(auth_key, data[index]))
#
#         elif isinstance(data, dict):
#             for key in data:
#                 if isinstance(data[key], dict):
#                     to_list(None, data[key])
#                 elif isinstance(data[key], list):
#                     to_list(key, data[key])
#                 else:
#                     if data[key] is None:  # 空为真
#                         pass
#                     else:
#                         param_array.append("{}={}".format(key, data[key]))
#         else:
#             print("签名参数异常")
#
#     to_list(auth_key, data)
#     new_param = "&".join(sorted(param_array))
#     authentication = hashlib.md5(new_param.encode(encoding='UTF-8')).hexdigest().upper()
#     return authentication

# if __name__ == '__main__':
#     dict1 = {'accountNo': 'T9-TServer', 'secretCode': 'fbw77t42dlb3cw6z', 'timestamp': 1568183260127,
#              'data': {'newPhoneNumber': '18201112814',
#                       'uuid': 'd600c89bb4ff8c6528a1e91650d93e3e37d6799ed03edb125fd86b439a5969bc'}}
#     print(sign.get_authentication(None, dict1))













