#!/usr/bin/env python
# coding=utf-8

from libs import util
from libs.conn_db_direct import Conn2DbDirect
import pymysql
import sqlparse

pymysql.install_as_MySQLdb()

conf = util.conf_path()


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

        return Dataset
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def __str__(self):
        return ''