# -*- coding: utf-8 -*-

from base  import Base

class SlowSQL:
    def __init__(self):
        self.client = Base()


    def query(self):
        url='https://rds.aliyuncs.com/?Action=DescribeSlowLogRecords' \
            '&DBInstanceId=riauvjz6zajfiq6ba1370329449201' \
            '&StartTime=2011-06-11T15:00Z' \
            '&EndTime=2011-06-11T16:00Z' \
            '&<公共请求参数>'
