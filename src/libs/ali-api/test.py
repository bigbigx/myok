import xrange
import bcolors
import time
import random
import randstr
import cursor

def  create_db_table():
    sql = 'CREATE TABLE if not exists t1(id int unsigned primary key auto_increment not null , age tinyint unsigned , name VARCHAR(128) , gmt_created dat    etime NOT NULL , msg text)'
    try:
       cursor.execute(sql)
    except Exception as e:
       print("excute %s error,"%sql, e)

def insert(cursor, svr, ibcx):
    commit_num = 500

    print(bcolors.OKGREEN + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) + \
          ' ' + svr + ' sarting insert into for 50000 --> %d --> 500' \
          % (ibc    x) + bcolors.ENDC)

    isql = "INSERT INTO t1( age , name , gmt_created , msg ) VALUES"
    cursor.execute('BEGIN')

    for v in xrange(commit_num):

        age = random.randint(1, 128)
        # import pdb
        # pdb.set_trace()
        rndstr = randstr(age)
          # print '*************',rndstr

        sql = '( ' + str(age) + ' , \'' + rndstr + '\'' + ',\'' + time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                time.localtime()) + '\' , \'' + rndstr * 3 + '\')'
        if v == 0:
            isql = isql + sql
        else:

            isql = isql + ' , ' + sql

        cursor.execute(isql)

        cursor.execute('COMMIT')


def init(cursor, svr):
    timestamp = time.time()
    pool_num = 50000
    ibcx = 0
    for x in xrange(100):
        ibcx += 500
    insert(cursor, svr, ibcx)

    print(bcolors.WARNING + time.strftime('%Y-%m-%d %H:%M:%S',
                                    time.localtime()) + ' ' + svr + ' Init_data successful using time %d seconds' % (i                                                                                                                    nt( time.time() ) - int(
        timestamp)) + bcolors.ENDC)