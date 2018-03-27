#!/usr/bin/env python
# coding=utf-8

# from libs import util
# from libs.conn_db_dir
# ect import Conn2DbDirect
import pymysql
import sqlparse

pymysql.install_as_MySQLdb()

# conf = util.conf_path()


class Explain(object):
    def __init__(self, LoginDic=None):
        self.__dict__.update(LoginDic)
        self.con = object

    def __enter__(self, LoginDic=None):
        #print(self.__dict__)
        self.con = pymysql.connect(host=self.__dict__['host'],
                                   user=self.__dict__['user'],
                                   passwd=self.__dict__['password'],
                                   port=int(self.__dict__['port']),
                                   db=self.__dict__['db'],
                                   charset="utf8")
        return self

    def ShowExplain(self, sql=None):
        sql=''' explain  ''' + sql
        print(sql)
        with self.con.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            Dataset = [
                {
                    'select_type': row[1],
                    'table': row[2],
                    'type': row[3],
                    'possiblekeys': row[4],
                    'key': row[5],
                    'key_len': row[6],
                    'ref': row[7],
                    'rows': row[8],
                    'extra': row[9]
                }
                for row in result
            ]
        cursor.close()
        return Dataset

    # / *受影响行数: 0
    # 已找到记录: 2
    # 警告: 0
    # 持续时间 1
    # 查询: 0.047 sec. * /
    def RunSQL(self,sql=None):
        with self.con.cursor() as cursor:
                cursor.execute(sql)
                self.con.commit()
        #         result = cursor.fetchall()
        #         print(result)
        #         Dataset = [
        #             {
        #                 'nums_affected ': row[1],  # 受影响行数
        #                 'record': row[2],  #已找到记录
        #                 'warning': row[3], #警告
        #                 'runtime': row[4], #持续时间
        #                 'querytime': row[5] #查询时间
        #             }
        #             for row in result
        #         ]
        # return Dataset

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def __str__(self):
        return ''



if __name__ == '__main__':

    with  Explain(
        LoginDic={
        'host': '101.236.41.66',
        'user': 'wang',
        'password': 'wang',
        'db': 'laimi_test',
        'port': 3306
    }) as test:
       # test.RunSQL(sql='''SELECT * FROM t_erp_sale_order t WHERE t.bill_id IN (11, 12);''')

       result = test.RunSQL(sql='''UPDATE t_erp_sale_order t SET t.delivery_status='cancel' WHERE t.bill_id IN (11, 12); UPDATE t_erp_sale_order t SET t.delivery_status='cancel' WHERE t.bill_id IN (11,12)''')
       print(result)
