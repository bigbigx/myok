#!/usr/bin/env python
#coding=utf-8


import urllib.request, urllib.parse, urllib.error
import http.cookiejar

cookie_filename = 'cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
cookie.load(cookie_filename, ignore_discard=True, ignore_expires=True)
print(cookie)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

get_url = 'https://rdsnew.console.aliyun.com/api/rds/DescribeBinlogFiles.json?DBInstanceId=rds6qxe126phmtspwi72&EndTime=2018-04-28T07:07:10Z&PageNumber=2&StartDateInit=%222018-04-20T16:00:10.234Z%22&StartTime=2018-04-20T16:00:10Z&__preventCache=1524899585995&currentPage=2&pageSize=100'  # 利用cookie请求訪问还有一个网址
get_request = urllib.request.Request(get_url)
get_response = opener.open(get_request)
print(get_response.read().decode())

# import cookielib
# import urllib2
# # 设置保存cookie的文件，同级目录下的cookie.txt
# filename = 'cookie.txt'
# # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
# cookie = cookielib.MozillaCookieJar(filename)
# # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
# handler = urllib2.HTTPCookieProcessor(cookie)
# # 通过handler来构建opener
# opener = urllib2.build_opener(handler)
# # 创建一个请求，原理同urllib2的urlopen
# response = opener.open("http://www.baidu.com")
# # 保存cookie到文件
# cookie.save(ignore_discard=True, ignore_expires=True)

def getHeaders(fileName):
    headers = []
    headList = ['User-Agent','Cookie']
    with open(fileName,'r') as fp:
        for line in fp.readlines():
            name,value = line.split(':',1)
            if name in headList:
                headers.append((name.strip(),value.strip()))
    return headers
#
# if __name__ == '__main__':
#     pass
    # headers = getHeaders('headersRaw.txt')
    # print(headers)