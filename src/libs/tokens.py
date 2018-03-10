#!/usr/bin/env python
#coding=utf-8
# serializer for JWT
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from libs import util
import time

#conf = util.conf_path()
"""
    token is generated as the JWT protocol.
    JSON Web Tokens(JWT) are an open, industry standard RFC 7519 method
"""

import time
import base64
import hmac
import sqlite3

#  产生token
def generate_token(key, expire=3600):
    r'''
        @Args:
            key: str (用户给定的key，需要用户保存以便之后验证token,每次产生token时的key 都可以是同一个key)
            expire: int(最大有效时间，单位为s)
        @Return:
            state: str
    '''
    ts_str = str(time.time() + expire)
    ts_byte = ts_str.encode("utf-8")
    sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
    token = ts_str+':'+sha1_tshexstr
    b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
    return b64_token.decode("utf-8")
# 将产生的token保存到数据库中，后面的session 的token与数据库中保留的token进行对比，

def create2sqlite(sql):
    conn = sqlite3.connect('token.db', isolation_level="IMMEDIATE", timeout=60, check_same_thread=False)
    c = conn.cursor()
    # '''执行语句''
    #sql = '''create table students (
    #        name text,
    #        username text,
    #        id int)'''
    c.execute(sql)
    # '''使用游标关闭数据库的链接'''
    c.close()


def insert2sqlite(sql):
    conn = sqlite3.connect('mytest.db')
    cursor = conn.cursor()
    print('hello SQL')
    while True:
        name = input('student\'s name')
        username = input('student\'s username')
        id_num = input('student\'s id number:')
        # '''insert语句 把一个新的行插入到表中'''

        #sql = ''' insert into students
        #          (name, username, id)
        #          values
        #          (:st_name, :st_username, :id_num)'''
        # 把数据保存到name username和 id_num中
        cursor.execute(sql, {'st_name': name, 'st_username': username, 'id_num': id_num})
        conn.commit()
        cont = ('Another student? ')
        if cont[0].lower() == 'n':
            break
    cursor.close()


import sqlite3
import os
def querysqlite(sql):

    os.chdir('d:\\pycharm\\lesson\\sn01')
    # conn = sqlite3.connect('D:\\pycharm\\lesson\\sn01\\SQL\\mytest.db')
    conn = sqlite3.connect(r'./SQL/mytest.db')
    cursor = conn.cursor()
    # 查询所有的学生表
    # sql = '''select * from students'''

    ''' 得到数据库中的名字'''
    #sql = "select rowid,  username from students"
    # 执行语句
    results = cursor.execute(sql)
    # 遍历打印输出
    all_students = results.fetchall()
    for student in all_students:
        print(student)

# 验证token
def certify_token(key, token):
    r'''
        @Args:
            key: str
            token: str
        @Returns:
            boolean
    '''
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    token_list = token_str.split(':')
    if len(token_list) != 2:
        return False
    ts_str = token_list[0]
    if float(ts_str) < time.time():
        # token expired
        return False
    known_sha1_tsstr = token_list[1]
    sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
    calc_sha1_tsstr = sha1.hexdigest()
    if calc_sha1_tsstr != known_sha1_tsstr:
        # token certification failed
        return False
    # token certification success
    return True

if __name__ == '__main__':
    key = "JD98Dskw=23njQndW9D"
    # 一小时后过期
    token = generate_token(key, 3600)

    print(certify_token(key, token))