# -*- coding: utf-8 -*-
import pymysql
import os
import configparser
from common.myLogger import logger


config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.dirname(__file__)) + '/cfg/config.ini')
mysql_status = config.get("base_para", "mysql_status")


class Mysql(object):
    def __init__(self):
        self.host = config.get("MYSQL", "host")
        self.port = eval(config.get("MYSQL", "port"))
        self.user = config.get("MYSQL", "user")
        self.password = config.get("MYSQL", "password")
        self.db = config.get("MYSQL", "db")
        self._conn = self.get_conn()
        self._cursor = self._conn.cursor()

    # 数据库连接
    def get_conn(self):
        try:
            conn = pymysql.connect(host=self.host,
                                   user=self.user,
                                   passwd=self.password,
                                   db=self.db,
                                   port=self.port,
                                   charset='utf8')
        except pymysql.Error as e:
            logger.error("Connect database failed.{}".format(e))
            conn = False
        return conn

    # 获取查询结果集
    def select_all(self, sql):
        try:
            self._cursor.execute(sql)
            res = self._cursor.fetchall()
            self._conn.commit()
            logger.debug("SQL语句【{}】，执行结果【{}】".format(sql, res))
        except pymysql.Error as e:
            res = False
            logger.warn("Select database exception:{}".format(e))
        return res

    # 获取查询结果集
    def select_one(self, sql):
        try:
            self._cursor.execute(sql)
            res = self._cursor.fetchone()  # 获取第一行数据
            # res = self._cursor.fetchmany(3)  # 获取前n行数据
            self._conn.commit()
            logger.debug("SQL语句【{}】，执行结果【{}】".format(sql, res))
        except pymysql.Error as e:
            res = False
            logger.warn("Select database exception.{}".format(e))
        return res

    def update(self, sql):
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            logger.debug("SQL语句【{}】，执行结果【{}】".format(sql, "True"))
            # logger.debug("Update database successfully")
        except pymysql.Error as e:
            logger.warn("Update database exception.{}".format(e))
            self._conn.rollback()
            return False
        return True

    # 关闭数据库连接
    def close(self):
        try:
            self._cursor.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源
        except pymysql.Error as e:
            logger.warn("Close database exception.{}".format(e))


class Mysql1(object):
    def __init__(self):
        pass

    # 数据库连接
    def get_conn(self):
        pass

    # 获取查询结果集
    def select_all(self, sql):
        pass

    # 获取查询结果集
    def select_one(self, sql):
        pass

    def update(self, sql):
        pass

    # 关闭数据库连接
    def close(self):
        pass


if mysql_status == '1':
    mysql = Mysql()
else:
    mysql = Mysql1()

if __name__ == "__main__":
    # mysql = Mysql()
    sql = "select  count(*) from  new_authed_user;"
    all = mysql.select_all(sql)
    print(all)

