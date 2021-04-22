# -*- coding: utf-8 -*-
from common.myMysql import mysql


def create_table():
    # 使用预处理语句创建表
    sql = """CREATE TABLE `test_case` (
      `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '序号',
      `suite_number` varchar(300) NOT NULL COMMENT '用例集编号',
      `case_number` varchar(300) NOT NULL UNIQUE COMMENT '用例编号',
      `module` varchar(300) DEFAULT NULL COMMENT '所属模块',
      `name` varchar(300) DEFAULT NULL COMMENT '接口名称',
      `description` varchar(300) DEFAULT NULL COMMENT '描述',
      `url` varchar(300) NOT NULL COMMENT '请求url',
      `method` varchar(20) NOT NULL COMMENT '请求方式',
      `headers` text DEFAULT NULL COMMENT '请求头部',
      `depend_key` varchar(300) DEFAULT NULL COMMENT '依赖key',
      `data` text DEFAULT NULL COMMENT '请求数据',
      `rule` varchar(20) DEFAULT '相等' COMMENT '匹配规则',
      `expect_result` text DEFAULT NULL COMMENT '预期结果',
      `priority`  varchar(20) DEFAULT 'P4' COMMENT '优先级',
      `is_execute` varchar(20) DEFAULT 'Y' COMMENT '是否需要执行,N:不需要;Y:需要',
      `depend_value` varchar(300) DEFAULT NULL COMMENT '被依赖value',
      `response_data` text DEFAULT NULL COMMENT '响应数据',
      `code`  varchar(20) DEFAULT NULL COMMENT '状态码',
      `execute_result` varchar(20) DEFAULT NULL COMMENT '执行结果,0:未通过;1:通过;-1:未知异常',
      `execute_time` datetime DEFAULT NULL COMMENT '执行时间',
      `create_time` datetime DEFAULT NULL COMMENT'创建时间',
      `update_time` datetime DEFAULT NULL COMMENT'更新时间',
      `remark` text DEFAULT NULL COMMENT '备注',
      `is_delete` bit(1) DEFAULT 0 COMMENT '是否删除,0:未删除;1:已删除',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='测试用例';
    """
    return mysql.update(sql)


def add_test_case():
    pass


if __name__ == '__main__':
    print(create_table())
    # add_test_case()
