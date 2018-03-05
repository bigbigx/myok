#!/usr/bin/env python
#coding=utf-8

import subprocess
import json
import pymysql

#  sql 语法优化
class sqladvisor:

    def sqlAdvisor(db_url, db_user, db_password, db_port, db_instance, sql_content):
        # sqladvisor  -h %s -u dbuser -p abc.1234 -P 3306 -d dbtest -q "select * from t2 where id=3;" -v 1
        cheungssh_info = {"status": False, "content": ""}
        cmd = ''' sqladvisor  -h %s -u %s -p %s -P %s -d %s -q " %s " -v  1''' % (
        db_url, db_user, db_password, db_port, db_instance, sql_content)
        data = {"result": ""}
        try:
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            stdout, stderr = popen.communicate()
            tmp = stdout.split("\n\n")
            data = ""
            for line in tmp:
                tmp_1 = line.split("[Note]")[-1]
                print
                tmp_1
                data = data + tmp_1 + "<br/>"
            # info=json.dumps(data,encoding="utf-8",ensure_ascii=False)
            info = json.dumps(data, ensure_ascii=False)

            cheungssh_info["status"] = True
            cheungssh_info["content"] = info
        except pymysql.Error as e:
            # print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            cheungssh_info["status"] = False
            cheungssh_info["content"] = str(e)
        print
        cheungssh_info
        return cheungssh_info