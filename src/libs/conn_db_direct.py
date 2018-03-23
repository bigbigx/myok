'''
直接连接数据库
'''
import pymysql

class Conn2DbDirect():

    def __init__(self,url,user,password,port):
        self.url = url
        self.user = user
        self.password = password
        self.port = port


    def __enter__(self):
        self.con = pymysql.connect(
            host=self.ip,
            user=self.user,
            passwd=self.password,
            db=self.db,
            charset='utf8mb4',
            port=self.port
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def execute(self, sql=None):
        with self.con.cursor() as cursor:
            sqllist = sql
            cursor.execute(sqllist)
            result = cursor.fetchall()
            self.con.commit()
        return result