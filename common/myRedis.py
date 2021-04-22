# coding=utf-8
import configparser
import os
import redis
from common.myLogger import logger

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.dirname(__file__)) + '/cfg/config.ini')
redis_status = config.get("base_para", "redis_status")


class Redis(object):
    def __init__(self):
        self.host = config.get("REDIS", "host")
        self.port = eval(config.get("REDIS", "port"))
        # self.password = config.get("REDIS", "password")
        self.r = self.get_conn()

    def get_conn(self):
        self.pool = redis.ConnectionPool(host=self.host,
                                         # password=self.password,
                                         port=self.port,
                                         decode_responses=True)
        r = redis.Redis(connection_pool=self.pool)
        return r

    def set_redis(self, skuid, stock_value):
        s = 'stock_%d_%s' % (100000, skuid)
        self.r.set(s, stock_value * 10000)

    def get_redis(self, skuid):
        s = 'stock_%d_%s' % (100000, skuid)
        # goodsstock = float(self.r.get(s))
        goodsstock = self.r.get('TojoyUser:mobile::18637607203')
        return goodsstock

    def del_redis(self, key_data):
        list_keys = self.r.keys(key_data)
        logger.debug("Redis to delete data【{}】".format(list_keys))
        for key in list_keys:
            res = self.r.delete(key)
            logger.debug("Redis delete data【{}】 Delete status【{}】".format(key, res))


class Redis1(object):
    def __init__(self):
        pass

    def get_conn(self):
        pass

    def set_redis(self, skuid, stock_value):
        pass

    def get_redis(self, skuid):
        pass

    def del_redis(self, key_data):
        pass


if redis_status == '1':
    my_redis = Redis()
else:
    my_redis = Redis1()

if __name__ == '__main__':
    key = "TojoyUser:mobile::144*"
    my_redis.del_redis(key)
