import sqlite3
import os

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



def query(sql):

    os.chdir('d:\\pycharm\\lesson\\sn01')
    # conn = sqlite3.connect('D:\\pycharm\\lesson\\sn01\\SQL\\mytest.db')
    conn = sqlite3.connect(r'./SQL/mytest.db')
    cursor = conn.cursor()
    # 查询所有的学生表
    # sql = '''select * from students'''

    ''' 得到数据库中的名字'''
    #sql = "select rowid,  username from students"
    # 执行语句
    result = False
    results = cursor.execute(sql)
    # 遍历打印输出
    hello = results.fetchall()
    if hello:
        result = True

    return result