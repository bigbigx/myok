import sqlite3
import logging
import os

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

def create_table(sql):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    cursor.close()
    conn.close()



def add_one(username,workid,token):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    try:
        insert_sql ="insert into token_db_new values(?, ?, ?) "
        param = (username,workid,token)
        cursor.execute(insert_sql,param)
        conn.commit()
    except Exception as e:
        print(e)
        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
    cursor.close()
    conn.close()


def add_many(value : [],table_namme):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    try:
        cursor.executemany("insert into  token_db_new  values ();", value)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        conn.rollback()
    cursor.close()
    conn.close()


def deleteByToken(token):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    try:
        cursor.execute("delete from token_db_new where token ='%s' " % (token))
        conn.commit()
    except Exception as e:
        print(e)
        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        conn.rollback()
    cursor.close()
    conn.close()

def delete(username, workid):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    try:
        cursor.execute("delete from token_db_new where username ='%s' and workid ='%s'" % (username, workid))
        conn.commit()
    except Exception as e:
        print(e)
        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        conn.rollback()
    cursor.close()
    conn.close()

def queryByToken(token):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    query_sql = "select token from  token_db_new where token='%s'" % (token)
    # 执行语句
    result = False
    results = cursor.execute(query_sql)
    # 遍历打印输出
    hello = results.fetchall()
    if hello:
        result = True
    print(result)
    return result


def query(username,workid):

    #os.chdir('d:\\pycharm\\lesson\\sn01')
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    query_sql = "select token from  token_db_new where username='%s' and workid='%s'" % (username, workid)
    # 执行语句
    result = False
    results = cursor.execute(query_sql)
    # 遍历打印输出
    hello = results.fetchall()
    if hello:
        result = True
    print(result)
    return result