#!/usr/bin/env python
#coding=utf-8
'''

Some tool sets

2017-11-23

cookie

'''

#from urllib import request

import urllib
from collections import namedtuple
import json
import random
import ssl
import time
import ldap3
import configparser
import hashlib
import random,string

#def dingding(content: str = None, url: str = None):
def dingding(content = None, url = None):
    '''
    dingding webhook 
    '''
    pdata = {"msgtype": "text", "text": {"content": content}}
    binary_data = json.dumps(pdata).encode(encoding='UTF8')
    headers = {"Content-Type": "application/json"}
    req = request.Request(url, headers=headers)
    context = ssl._create_unverified_context()
    request.urlopen(req, data=binary_data, context=context).read()


#def date() -> str:
def date():
    '''
    datetime
    '''
    now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    return now


#def workId() -> str:
def workId():
    '''
    工单
    '''
    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    _ran = ''.join(random.sample('0123456789', 4))

    now = f'{now}{_ran}'
    #now = '{now}{_ran}'
    return now

##  使用方法：  generateTokens(32)  生成32位的随机数
def generateTokens(length):
    #随机出数字的个数
    numOfNum = random.randint(1,length-1)
    numOfLetter = length - numOfNum
    #选中numOfNum个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    #选中numOfLetter个字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    #打乱这个组合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    #生成密码
    genPwd = ''.join([i for i in slcChar])
    return genPwd





#def ser(_obj: object) -> list:
def ser(_obj):
    '''
    orm.raw 序列化
    '''
    _list = []
    _get = []
    for i in _obj:
        _list.append(i.__dict__)

    for i in _list:
        del i['_state']
        _get.append(i)
    return _get


#def conf_path() -> object:
def conf_path():
    '''
    读取配置文件属性
    '''
    _conf = configparser.ConfigParser()
    _conf.read('deploy.conf')
    #_conf.read('/root/Yearning/src/deploy.conf')
    conf_set = namedtuple("name", ["db", "address", "port", "username", "password", "ipaddress",
                                   "inc_host", "inc_port", "inc_user", "inc_pwd", "backupdb",
                                   "backupport", "backupuser", "backuppassword","ladp_server",
                                   "ldap_scbase","ladp_domain", "mail_user","mail_password","smtp"])

    return conf_set(_conf.get('mysql', 'db'), _conf.get('mysql', 'address'),
                    _conf.get('mysql', 'port'), _conf.get('mysql', 'username'),
                    _conf.get('mysql', 'password'), _conf.get('host', 'ipaddress'),
                    _conf.get('Inception', 'ip'), _conf.get('Inception', 'port'),
                    _conf.get('Inception', 'user'), _conf.get('Inception', 'password'),
                    _conf.get('Inception', 'backupdb'), _conf.get('Inception', 'backupport'),
                    _conf.get('Inception', 'backupuser'), _conf.get('Inception', 'backuppassword'),
                    _conf.get('LDAP','LDAP_SERVER'),_conf.get('LDAP','LDAP_SCBASE'),_conf.get('LDAP','LDAP_DOMAIN'),
                    _conf.get('email', 'username'), _conf.get('email', 'password'), _conf.get('email', 'smtp_server'))

def auth(username, password):
    conf = conf_path()
    LDAP_SERVER = conf.ladp_server
    LDAP_DOMAIN = conf.ladp_domain
    c = ldap3.Connection(
        ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL),
        user=username + '@' + LDAP_DOMAIN,
        password=password)
    ret = c.bind()
    if ret:
        c.unbind()
        return True
    else:
        return False

