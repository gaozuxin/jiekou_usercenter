# -*- coding: utf-8 -*-
import logging.handlers
import os
from common.formatTime import date_time_log


class Logger(object):
    def __init__(self, path, clevel=logging.INFO, Flevel=logging.INFO):
        # 设置创建日志的对象
        self.logger = logging.getLogger(path)
        if logging.handlers:
            # 设置日志的最低级别低于这个级别将不会在屏幕输出，也不会保存到log文件
            self.logger.setLevel(logging.DEBUG)
            # 给这个handler选择一个格式（）
            fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
            # 设置终端日志 像终端输出的日志
            sh = logging.StreamHandler()
            sh.setFormatter(fmt)  # 设置个终端日志的格式
            sh.setLevel(clevel)  # 设置终端日志最低等级
            # 设置文件日志 用于向一个文件输出日志信息。不过FileHandler会帮你打开这个文件。
            fh = logging.FileHandler(path)
            fh.setFormatter(fmt)  # 设置个文件日志的格式
            fh.setLevel(Flevel)  # 设置终端日志最低等级
            self.logger.addHandler(sh)  # 增加终端日志Handler
            self.logger.addHandler(fh)  # 增加文件日志Handler

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def getlog(self):
        return self.logger


logger = Logger(os.path.dirname(os.path.dirname(__file__)) + '/result/logs/userCenter{}.log'.format(date_time_log()),
                logging.DEBUG, logging.DEBUG)
# if __name__ == '__main__':
#     logger.debug('一个debug信息')
#     logger.info('一个info信息')
#     logger.warn('一个warning信息')
#     logger.error('一个error信息')
#     logger.cri('一个致命critical信息')
