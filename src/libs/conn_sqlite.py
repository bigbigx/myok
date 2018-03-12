import sqlite3
import logging
import os

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

def create_table(sql):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    cursor.close()
    conn.close()



def add_one(value):
    conn = sqlite3.connect('d:\\token.db')
    cursor = conn.cursor()
    try:
        insert_sql ="insert into token_db_new values(?, ?, ?) "
        cursor.executemany(insert_sql, value)
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