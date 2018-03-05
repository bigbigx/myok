#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from docx import Document
from docx.shared import Inches
import xlwt
import xlrd
import pymysql


class DbInfo(object):
    host = ''
    user = ''
    password = ''
    database = ''
    charset = ''
    conn = None

    def __init__(self, host=None, user=None, password=None, database=None, charset=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    def connMysql(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            charset=self.charset
            )
        return self.conn

    def closesql(self):
        self.conn.close()

    def execute(self, sql=None):
        cur = self.connMysql()
        with cur.cursor() as cursor:
            sqllist = sql
            cursor.execute(sqllist)
            result = cursor.fetchall()
            self.conn.commit()
        return result


class toExcel:


    document = None


    def __init__(self, Host=None, User=None, Password=None, Database=None, Charset=None):
        self.turnOjb = DbInfo(
            host=Host,
            user=User,
            password=Password,
            database=Database,
            charset=Charset
        )
        self.createDoc()


    def createExcel(self):
        # 搜取所有结果
        results = cursor.fetchall()
        # 获取MYSQL里面的数据字段名称
        fields = cursor.description
        workbook = xlwt.Workbook(encoding='utf-8')  # workbook是sheet赖以生存的载体。
        sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

    def exportExcelAndMail(self):
        createExcel()



    def exportTables(self, Conn=None, Schemal=None, TableList=None):
        pass

    # 查询数据库，然后导出excel记录
    def export(host,user,pwd,db,sql):
            conn = MySQLdb.connect(host, user, pwd, db, charset='utf8')
        cursor = conn.cursor()
        count = cursor.execute(sql)
        print("查询出" + str(count) + "条记录")
        if count > 0:
            # 来重置游标的位置
            cursor.scroll(0, mode='absolute')
            # 搜取所有结果
            results = cursor.fetchall()
            # 获取MYSQL里面的数据字段名称
            fields = cursor.description
            workbook = xlwt.Workbook(encoding='utf-8')  # workbook是sheet赖以生存的载体。
            sheet = workbook.add_sheet(sheet_name, cell_overwrite_ok=True)
            # 写上字段信息
            for field in range(0, len(fields)):
                sheet.write(0, field, fields[field][0])
            # 获取并写入数据段信息
            row = 1
            col = 0
            for row in range(1, len(results) + 1):
                for col in range(0, len(fields)):
                    sheet.write(row, col, u'%s' % results[row - 1][col])
            workbook.save(out_path)
        else:
            print("无数据")


if __name__ == '__main__':
    toExcel()