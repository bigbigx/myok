from django.shortcuts import render
from dwebsocket.decorators import accept_websocket, require_websocket
from django.http import HttpResponse
import paramiko


#  命令的后台类
class mycommand():
    def __init__(self):
        pass

    def exec_command(comm):
        hostname = '你要连接的Linux服务器IP'
        username = '登陆的Linux账号'
        password = '登陆的Linux账号密码'

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(comm)
        result = stdout.read()
        ssh.close()
        return result

    @accept_websocket
    def echo_once(request):
        if not request.is_websocket():  # 判断是不是websocket连接
            try:  # 如果是普通的http方法
                message = request.GET['message']
                return HttpResponse(message)
            except:
                return render(request, 'index.html')
        else:
            for message in request.websocket:
                message = message.decode('utf-8')
                if message == 'backup_all':  # 这里根据web页面获取的值进行对应的操作
                    command = 'sh test.sh'  # 这里是要执行的命令或者脚本，我这里写死了，完全可以通过web页面获取命令，然后传到这里
                    request.websocket.send(exec_command(command))  # 发送消息到客户端
                else:
                    request.websocket.send('小样儿，没权限!!!'.encode('utf-8'))