#!/usr/bin/env python
#coding=utf-8
# __author__ = '戴儒锋'
# http://www.linuxyw.com
"""
    执行代码前需要安装
    pip install bottle
    pip install websocket-client
    pip install bottle-websocket
"""
from bottle import get, run
import paramiko
from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket
users = set()   # 连接进来的websocket客户端集合
@get('/websocket/', apply=[websocket])
def chat(ws):
    users.add(ws)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('43.241.232.104', 22, 'root', 'q9mQ7axgjPaY', timeout=15)
    ssh_t = ssh.get_transport()
    chan = ssh_t.open_session()
    # chan.get_pty()
    # chan.setblocking(0)  # 设置非阻塞
    cmd = "tailf /var/log/nginx/access.log"
    chan.exec_command(cmd)
    while True:

        msg = ws.receive()  # 接客户端的消息
        print(msg)
        if msg != 'quit':
            for u in users:
                # u.send(msg) # 发送信息给所有的客户端
                log_msg = chan.recv(10000).strip().decode() + '\n'  # 接收日志信息
                # log_msg = chan.recv(10000).strip()
                u.send(log_msg)  # 发送信息给所有的客户端
        else:
            break
    # 如果有客户端断开连接，则踢出users集合
    users.remove(ws)
run(host='0.0.0.0', port=3320, server=GeventWebSocketServer)