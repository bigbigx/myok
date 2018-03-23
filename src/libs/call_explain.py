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
        self.con = pymysql.connect(host=LoginDic['host'],
                                   user=LoginDic['user'],
                                   passwd=LoginDic['password'],
                                   port=int(LoginDic['port']),
                                   db=LoginDic['db'],
                                   charset="utf8")
        return self

    def ShowExplain(self, sql):
        # select_type = ''
        # table = ''
        # type = ''
        # possible_keys = ''
        # key = ''
        # key_len = ''
        # rows = ''
        # ref = ''
        # extra = ''
        # #result = {'select_type': select_type, 'table': table, 'type': type, 'possible_keys': possible_keys, 'key': key,
        # #          'key_len': key_len, 'ref': ref, 'rows': rows, 'extra': extra}
        # #tmp = Conn2DbDirect.execute("explain %s" % sql)
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