# -*- coding: utf-8 -*-
import time


def date_time_chinese():  # 2019年09月09日 17时02分19秒
    return time.strftime("%Y{y}%m{m}%d{d} %H{h}%M{f}%S{s}", time.localtime()).format(y='年', m='月', d='日',
                                                                                     h='时', f='分', s='秒')


def date_time():  # 2019-09-09 17:02:19
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def date_time_log():  # 2019-09-09
    return time.strftime("%Y-%m-%d", time.localtime())


if __name__ == '__main__':
    print(date_time_chinese())
    print(date_time())
    print(date_time_log())
