#!/usr/bin/env python
#coding=utf-8

from datetime import datetime
from docx import Document
from docx.shared import Inches
import xlwt
import xlrd
import pymysql
import datetime
import time
#from libs import util

#conf = util.conf_path()

def exportExcel(host,user,password,dbname,port,sql,outputpath):
    conn = pymysql.connect(host,user,password,dbname,port,charset='utf8')
    cursor = conn.cursor()
    count = cursor.execute(sql)
    # 重置游标的位置
    #cursor.scroll(0,mode='absolute')
    # 搜取所有结果
    results = cursor.fetchall()
    cursor.close()
    cursor.close()
    # 获取MYSQL里面的数据字段名称
    fields = cursor.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_'+table_name,cell_overwrite_ok=True)

    # 写上字段信息
    for field in range(0,len(fields)):
        sheet.write(0,field,fields[field][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1,len(results)+1):
        for col in range(0,len(fields)):
            sheet.write(row,col,u'%s'%results[row-1][col])

    workbook.save(outputpath)

def execude_sql(SQL):  #定义一个执行SQL的函数
    con = pymysql.connect('ip','用户','密码','指定数据库',charset='utf8') #连接数据库
    cur = con.cursor()  #定义一个游标　
    cur.execute(SQL)#执行指定SQL
    result = cur.fetchall()
    cur.close()
    con.close()
#execude_sql('select id,name from student where class =1024') #调用函数，查询class=1024的id和name

#def wite_to_excel(name):
    filename = name + '.cvs'  #定义Excel名字
    wbk = xlwt.Workbook()  #实例化一个Excel
    sheet1 = wbk.add_sheet('result',cell_overwrite_ok=True) #添加该Excel的第一个sheet，如有需要可依次添加sheet2等
    sheet1.write(0, filed, fileds[i], set_style('宋体', '200', True))
    fileds = [u'ID编号',u'名字'] #直接定义结果集的各字段名
    execude_sql(1024)  #调用函数执行SQL，获取结果集
    for filed in range(0,len(fileds)):   #写入字段信息
        sheet1.write(0,filed,fileds[i])
    for row in range(1,len(result)+1):  #写入SQL查询数据
        for col in range(0,len(fileds)):
            sheet1.write(row,col,result[row-1][col])
    wbk.save(filename)  #保存Excel

def set_style(name,height,bold=False):
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() # 为样式创建字体
    # font.name = name # 'Times New Roman'
    font.bold = bold  #是否加粗，默认不加粗
    font.color_index = 4
    font.height = height  #定义字体大小
    style.font = font

    alignment = xlwt.Alignment() #创建居中
    alignment.horz = xlwt.Alignment.HORZ_CENTER #可取值: HORZ_GENERAL, HORZ_LEFT, HORZ_CENTER, HORZ_RIGHT, HORZ_FILLED, HORZ_JUSTIFIED, HORZ_CENTER_ACROSS_SEL, HORZ_DISTRIBUTED
    alignment.vert = xlwt.Alignment.VERT_CENTER # 可取值: VERT_TOP, VERT_CENTER, VERT_BOTTOM, VERT_JUSTIFIED, VERT_DISTRIBUTED
    style.alignment = alignment # 文字居中

if __name__ == '__main__':
    sql="select * from t_erp_sale_order t where t.bill_id='13';"
    outputpath='d:\\jianglb111.xls'
    host='101.236.41.66'
    user='jianglb'
    password='jianglb'
    dbname='laimi_test'
    port=3306
    table_name=''
    exportExcel(host, user, password, dbname,port, sql, outputpath)