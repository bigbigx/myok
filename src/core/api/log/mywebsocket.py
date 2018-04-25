from threading import Thread
import struct
# import time
import hashlib
import sys
import base64
import socket
import time
import paramiko

# from core.models import HostUserPwd

class returnCrossDomain(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.con = connection
        self.isHandleShake = False
        self.close_flag=False

    def run(self):  #  增量文件内容
        while True:
            if not self.isHandleShake:
                # 开始握手阶段
                print('handshake')
                header = self.analyzeReq()
                secKey = header['Sec-WebSocket-Key'];

                acceptKey = self.generateAcceptKey(secKey)

                response = "HTTP/1.1 101 Switching Protocols\r\n"
                response += "Upgrade: websocket\r\n"
                response += "Connection: Upgrade\r\n"
                response += "Sec-WebSocket-Accept: %s\r\n\r\n" % (acceptKey.decode('utf-8'))
                self.con.send(response.encode())
                self.isHandleShake = True
                print('response:\r\n' + response)
                # 握手阶段结束
            else:
                # 接受客户端数据
                try:
                    opcode = self.getOpcode()
                    if opcode == 8:
                        self.con.close()
                    self.getDataLength()
                    clientData = self.readClientData()
                    print('客户端数据：' + clientData)
                    self.sendDataToClient('Connected Successlly \n')
                    ssh = paramiko.SSHClient()
                    # 接受客户端的参数，连接ssh,然后执行taif 命令，将结果返回到客户端
                    if clientData != 'quit':
                        msg_list = clientData.split(";")
                        ip = ''.join(msg_list[0].split(':')[1:])
                        print(ip)
                        # user= getUserPwdByIP(ip,'root',1)['username']
                        user ='root'
                        # password = getUserPwdByIP(ip,'root',1)['password']
                        password='q9mQ7axgjPaY'
                        path = ''.join(msg_list[1].split(':')[1:])
                        print(path)
                        keyword = ''.join(msg_list[2].split(':')[1:])
                        print(keyword)

                        cnum = ''.join(msg_list[3].split(':')[1:])
                        type = ''.join(msg_list[4].split(':')[1:])
                        print(type)

                        # ssh=get_ssh(ip, user, password)
                        if type == "0": # 增量文件 使用命令 tail -n 40 -f
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect('43.241.232.104', 22, 'root', 'q9mQ7axgjPaY', timeout=15)
                            # ssh.connect('43.241.232.104', 22, 'root', 'q9mQ7axgjPaY')
                            try:
                                ssh_t = ssh.get_transport()
                                chan = ssh_t.open_session()
                                # chan.get_pty()
                                # chan.setblocking(0)  # 设置非阻塞
                                cmd = "tailf /var/log/nginx/access.log"
                                # if chan.active:
                                chan.exec_command(cmd)
                                while True:
                                        # tmp = chan.recv_ready()
                                        # print(tmp)
                                   while chan.recv_ready():
                                         log_msg = chan.recv(10000).strip().decode() + '\n'  # 接收日志信息
                                            # log_msg = chan.recv(10000).decode() + '\n'  # 接收日志信息
                                         print(log_msg)
                                         self.sendDataToClient(log_msg)
                                         if self.close_flag:
                                                print("停止循环")
                                                break
                                   if chan.exit_status_ready():
                                        break
                                break
                                    # print('next')
                            except Exception as e:
                                print('增量异常')
                                print(e)

                        elif type == "1":  # 全量内容 ,使用命令cat
                            # ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect('43.241.232.104', 22, 'root', 'q9mQ7axgjPaY', timeout=15)
                            # ssh.connect('43.241.232.104', 22, 'root', 'q9mQ7axgjPaY')
                            try:
                                ssh_t = ssh.get_transport()
                                chan = ssh_t.open_session()
                                # chan.get_pty()
                                # chan.setblocking(0)  # 设置非阻塞
                                # cmd = "nl /mnt/java/laimi-wms/logs/app.log"
                                cmd = "tailf /var/log/nginx/access.log"
                                # if chan.active:
                                chan.exec_command(cmd)
                                tmp = chan.recv_ready()
                                print(tmp)
                                    # while True:
                                while chan.recv_ready():
                                     tmp = chan.recv(10000).decode() + '\n'
                                    # chan.exec_command(cmd)
                                    # print(stdout.readlines())
                                     print(tmp)
                                    # time.sleep(5)
                                     self.sendDataToClient(tmp)
                                     break
                                    # if chan.exit_status_ready():
                                    #     break
                                chan.close()
                                ssh.close()
                                    # time.sleep(5)
                                # else:
                                #     print('Not active')
                            except Exception as e:
                                print('全量异常')
                                print(e)
                                # ssh.close()
                                # ssh.close()

                        else:
                            print("Oops！ 奇怪的事情，请联系系统管理员")
                            pass

                            # while 1:
                            #     if chan.exit_status_ready():
                            #         break
                            #
                            #     try:
                            #         recv = chan.recv(65536)
                            #         print(recv)
                            #     except KeyboardInterrupt:
                            #         chan.send("\x03")  # 发送 ctrl+c
                            #         chan.close()
                            #         ssh.close()   # exit 0
                            # while True:
                            #     print(chan.recv_ready())
                            #     while chan.recv_ready():
                            #         clientdata1 = self.readClientData()
                            #         print(clientdata1)
                            #         if clientdata1 is not None and 'quit' in clientdata1:
                            #             self.sendDataToClient(' Successlly')
                            #             break
                            #         log_msg = chan.recv(10000).strip()  # 接收日志信息
                            #         # print log_msg
                            #         self.sendDataToClient(log_msg)
                            #     if chan.exit_status_ready():
                            #         break
                            #     clientdata2 = self.readClientData()
                            #     if clientdata2 is not None and 'quit' in clientdata2:
                            #         self.sendDataToClient(' Successlly')
                            # break
                        # ssh.close()
                    else :  # 关闭信息
                        # if clientData is not None and 'quit' in clientData:
                        print('Begin to Close Connect \n')
                        self.sendDataToClient('Close Connect \n')
                        ssh.close()
                        print('Close Connect  Successly \n')
                        self.close_flag=True

                except Exception as e:
                    print('parent')
                    print(e)
                    # ssh.close()
        self.con.close()


    def analyzeReq(self):
        reqData = self.con.recv(1024).decode()
        reqList = reqData.split('\r\n')
        headers = {}
        for reqItem in reqList:
            if ': ' in reqItem:
                unit = reqItem.split(': ')
                headers[unit[0]] = unit[1]
        return headers

    def generateAcceptKey(self, secKey):
        sha1 = hashlib.sha1()
        sha1.update((secKey + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode())
        sha1_result = sha1.digest()
        acceptKey = base64.b64encode(sha1_result)
        return acceptKey

    def getOpcode(self):
        first8Bit = self.con.recv(1)
        first8Bit = struct.unpack('B', first8Bit)[0]
        opcode = first8Bit & 0b00001111
        return opcode

    def getDataLength(self):
        second8Bit = self.con.recv(1)
        second8Bit = struct.unpack('B', second8Bit)[0]
        masking = second8Bit >> 7
        dataLength = second8Bit & 0b01111111

        if dataLength <= 125:
            payDataLength = dataLength
        elif dataLength == 126:
            payDataLength = struct.unpack('H', self.con.recv(2))[0]
        elif dataLength == 127:
            payDataLength = struct.unpack('Q', self.con.recv(8))[0]
        self.masking = masking
        self.payDataLength = payDataLength

    def readClientData(self):
        if self.masking == 1:
            maskingKey = self.con.recv(4)
        data = self.con.recv(self.payDataLength)
        if self.masking == 1:
            i = 0
            trueData = ''
            for d in data:
                trueData += chr(d ^ maskingKey[i % 4])
                i += 1
            return trueData
        else:
            return data

    def sendDataToClient(self, text):
        sendData = ''
        sendData = struct.pack('!B', 0x81)

        length = len(text)
        if length <= 125:
            sendData += struct.pack('!B', length)
        elif length <= 65536:
            sendData += struct.pack('!B', 126)
            sendData += struct.pack('!H', length)
        elif length == 127:
            sendData += struct.pack('!B', 127)
            sendData += struct.pack('!Q', length)

        sendData += struct.pack('!%ds' % (length), text.encode())
        dataSize = self.con.send(sendData)

def getUserPwdByIP(ip, username,is_privateIP): # is_privateIP 访问方式。 是否私网IP 1--是  0 ---否
    user_pwd = {'username': 'root', 'password': 'q9mQ7axgjPaY'}
    # print('entry the getuser')
    # if is_privateIP == 0:
    #     obj = HostUserPwd.objects.filter(public_IP=ip, user_name=username).first()
    #     user_pwd = {'username': username, 'password': obj.password}
    # elif is_privateIP ==1:
    #     myobj = HostUserPwd.objects.filter(private_IP=ip, user_name=username).first()
    #     user_pwd = {'username': username, 'password': myobj.password}
    # else:
    #     pass

    return user_pwd

def get_ssh(ip, user, pwd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, 22, user, pwd, timeout=15)
        return ssh
    except Exception as e:
        print('异常')
        print(e)
    # return "False"

def test():
    # ssh = get_ssh('43.241.232.104', 'root', 'q9mQ7axgjPaY')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('43.241.232.104', 22,'root', 'q9mQ7axgjPaY', timeout=15)
    try:
        ssh_t = ssh.get_transport()
        chan = ssh_t.open_session()
        chan.get_pty()
        chan.setblocking(0)  # 设置非阻塞
        cmd = "tail -n 40 -f /var/log/nginx/access.log.1"
        if chan.active:
            chan.exec_command(cmd)
            tmp = chan.recv(1024).decode() + '\n'
            # chan.exec_command(cmd)
            # print(stdout.readlines())
            print(tmp)
        else:
            print('Nothing')

    except Exception as e:
        print('异常')
        print(e)

def main():
    print('start')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('127.0.0.1', 3320))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.listen(5)
    print(sock)
    while True:
        try:
            print('entry')
            connection, address = sock.accept()
            print(connection)
            print(address)
            returnCrossDomain(connection).start()
            print('111')
        except:
            time.sleep(1)


if __name__ == "__main__":
    main()
    # test()