# coding:utf-8
import os
import sys
import struct
import base64
import hashlib
import socket
import threading
import paramiko
#import simplejson

# from  asset.assets_controler  import ControlerCenter


def get_ssh(ip, user, pwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, user, pwd, timeout=15)
        return ssh
    except Exception as e:
        print("异常")
        print(e)
        # return "False"


def recv_data(conn): # 服务器解析浏览器发送的信息
    try:
        # all_data = conn.recv(1024).decode('utf-8', 'ignore')
        all_data = conn.recv(1024).decode('utf-8')
        # all_data = conn.recv(1024).decode('base64','strict')
        # all_data = conn.recv(1024).decode()

        print("start next")
        print(all_data)
        if not len(all_data):
            return False
    #dic = simplejson.loads(all_data)
    # print "hello"
    # print dic
    except Exception as e:
        print('nonononono')
        print(e)
    else:
      code_len = ord(all_data[1]) & 127
      if code_len == 126:
          masks = all_data[4:8]
          data = all_data[8:]
      elif code_len == 127:
          masks = all_data[10:14]
          data = all_data[14:]
      else:
          masks = all_data[2:6]
          data = all_data[6:]
      raw_str = ""
      i = 0
      for d in data:
          raw_str += chr(ord(d) ^ ord(masks[i % 4]))
          i += 1
      print("begin")
      print(raw_str)
      print("end")
      return raw_str


def send_data(conn, data):  # 服务器处理发送给浏览器的信息
    if data:
        data = str(data)
        print(data)
    else:
        return False
    token = "\x81"
    length = len(data)
    if length < 126:
        token += struct.pack("B", length).decode()  # struct为Python中处理二进制数的模块，二进制流为C，或网络流的形式。
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length).decode()
    else:
        token += struct.pack("!BQ", 127, length).decode()
    data = '%s%s' % (token, data)
    conn.send(data.encode('utf-8'))
    return True


def handshake(conn, address, thread_name):
    headers = {}
    shake = conn.recv(1024)
    if not len(shake):
        return False
    print('%s : Socket start handshaken with %s:%s' % (thread_name, address[0], address[1]))
    print(shake)
    # tmp = str(shake)
    # tmp1 = tmp[2:-1]
    # print(tmp1)
    header, data = shake.decode().split('\r\n\r\n', 1)
    for line in header.split('\r\n')[1:]:
        key, value = line.split(': ', 1)
        headers[key] = value
    if 'Sec-WebSocket-Key' not in headers:
        print('%s : This socket is not websocket, client close.' % thread_name)
        conn.close()
        return False
    MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    HANDSHAKE_STRING = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade:websocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: {1}\r\n" \
                       "WebSocket-Origin: {2}\r\n" \
                       "WebSocket-Location: ws://{3}/\r\n\r\n"
    sec_key = headers['Sec-WebSocket-Key']
    tmp = (sec_key + MAGIC_STRING).encode("utf-8")
    res_key = base64.b64encode(hashlib.sha1(tmp).digest())
    print(res_key)
    str_handshake = HANDSHAKE_STRING.replace('{1}', res_key.decode()).replace('{2}', headers['Origin']).replace('{3}',
                                                                                                       headers['Host'])
    conn.send(str_handshake.encode('utf-8'))
    print('%s : Socket handshaken with %s:%s success' % (thread_name, address[0], address[1]))
    print('Start transmitting data...')
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
    return True




#  publicIP 是外网IP
def  get_username_and_password(publicIP):
    user_pwd = {'username': 'root', 'password':'NtpxyH9NuqG3'}
    return user_pwd

def dojob(conn, address, thread_name):
  goahead=handshake(conn, address, thread_name)# 握手
  print('ppppppppppppppp')
  print(goahead)
  if goahead is not True:
      sys.exit(1)


  #print conn
  #print goahead
  conn.setblocking(0) # 设置socket为非阻塞
  #user=getUserName(ip)
  user="root"
  #password=getPassword(ip)
  password="q9mQ7axgjPaY"
  ssh = get_ssh('43.241.232.104', 'root', 'q9mQ7axgjPaY')# 连接远程服务器
  print(ssh)
  try:
      ssh_t = ssh.get_transport()
      chan = ssh_t.open_session()
      chan.setblocking(0)  # 设置非阻塞
      chan.exec_command('date')
  except Exception as e:
      print(e)


  while True:

    user=""
    password=""
    ip=""
    path=""
    keyword=""
    cnum=""

    clientdata11 = recv_data(conn)
    print(clientdata11)
    if clientdata11 is not None and 'myip' in clientdata11:#初始化的时候，数据传递过来
      msg=clientdata11
      print(msg)
      send_data(conn, '恭喜，服务端成功接收客户端信息')
      msg_list=msg.split(";")
      ip = ''.join(msg_list[0].split(':')[1:])
      path = ''.join(msg_list[1].split(':')[1:])
      keyword =  ''.join(msg_list[2].split(':')[1:])
      cnum =  ''.join(msg_list[3].split(':')[1:])

      if  ip =="" or ip is None:
          send_data(conn, '抱歉！  IP 地址没有传递过来！')
      #if get_username_and_password(ip)["status"] == 0:
      #   print "没有找到此IP对应的主机用户和密码信息"


      # user=get_username_and_password(ip)["username"]
      user='root'
      print("user: %s" % (user))
      # password=get_username_and_password(ip)["password"]
      password='q9mQ7axgjPaY'
      print("password: %s" % (password))
      #user="root"
      #password="q9mQ7axgjPaY"
    else:
      send_data(conn, ' -_-  抱歉，服务端没有接收到信息！')
      break


    ssh = get_ssh(ip,user,password)# 连接远程服务器
    show_str='''
           接的IP为:%s , 文件路径为:%s , 搜索关键字为:%s, grep上下行数为:%s 
          正在获取日志信息，请稍等。。。。。请不要着急！  如果比较急的话，建议提前启动日志窗口！
     '''  % ( ip,path,keyword,cnum)
    send_data(conn,show_str)
    #send_data(conn, '连接的IP为:%s , 文件路径为:%s , 搜索关键字为:%s, grep上下行数为:%s ' % ( ip,path,keyword,cnum))
    #send_data(conn,' 正在获取日志信息，请稍等。。。。。请不要着急！  如果比较急的话，建议提前启动日志窗口！ ')
    ssh_t = ssh.get_transport()
    chan = ssh_t.open_session()
    chan.setblocking(0)  # 设置非阻塞
    #chan.exec_command('tail -n 40  /var/log/nginx/access.log.1| grep "error" ')
    #chan.exec_command('tailf  /var/log/nginx/access.log.1|grep 200')
    cmd=""
    if keyword is None or keyword.strip()=="":
        if cnum is None or cnum.strip()=="":
            cmd='tailf %s' % (path)
        else:
            break
    else:
        if cnum is None or cnum.strip()=="":

            cmd='tailf %s |grep %s' % (path,keyword)
        else:
            cmd='tailf %s |grep -C%s  %s' % (path,cnum,keyword)
    cmd = 'tail -n 40 -f /var/log/nginx/access.log.1'
    chan.exec_command(cmd)

    while True:
        clientdata = recv_data(conn)
        if clientdata is not None and 'quit' in clientdata:# 但浏览器点击stop按钮或close按钮时，断开连接
           print('%s : Socket close with %s:%s' % (thread_name, address[0], address[1]))
           send_data(conn, 'close connect')
           conn.close()
           break

        while True:
             while chan.recv_ready():
                 clientdata1 = recv_data(conn)
                 if clientdata1 is not None and 'quit' in clientdata1:
                    print('%s : Socket close with %s:%s' % (thread_name, address[0], address[1]))
                    send_data(conn, 'close connect')
                    conn.close()
                    break
                 log_msg = chan.recv(10000).strip()# 接收日志信息
                 #print log_msg
                 send_data(conn, log_msg)
             if chan.exit_status_ready():
                 break
             clientdata2 = recv_data(conn)
             if clientdata2 is not None and 'quit' in clientdata2:
                 print('%s : Socket close with %s:%s' % (thread_name, address[0], address[1]))
                 send_data(conn, 'close connect')
                 conn.close()
                 break
        break
  #  else:
  #    print "clientdata  is None"
  #    send_data(conn, '前端传递过来的参数为空')
  #    break


def ws_service():
  index = 1
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:

    #sock.bind(('127.0.0.1', 3310))
    sock.bind(('0.0.0.0', 3310))
    sock.listen(1000)
    print('\r\n\r\nWebsocket server start, wait for connect!')
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
  except:
    print("Server is already running,quit")
    sys.exit()

  while True:
    #connection, address,ip,path,keyword = sock.accept()
    connection, address = sock.accept()
    print('hhhhhhhhhhhh')
    print(connection)
    print(address)
    #ip="172.16.187.127"
    #path="/var/log/nginx/access.log.1"
    #keyword=""
    #username=getUserName(ip)
    #password=getPassword(ip)

    thread_name = 'thread_%s' % index
    print ('%s : Connection from %s:%s' % (thread_name, address[0], address[1]))
    t = threading.Thread(target=dojob, args=(connection, address, thread_name))
    t.start()
    index += 1

ws_service()