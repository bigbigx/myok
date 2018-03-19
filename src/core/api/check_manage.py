# -*- coding=utf-8 -*-
import logging
from libs import baseview
from rest_framework.response import Response
from django.http import HttpResponse


CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

'''
常用的服务器检查命令
'''


class checkManage(baseview.BaseView):

    def get(self, request, args=None):
        try:
            page = request.GET.get('page')
            username = request.GET.get('username')
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                pass

            except Exception as e:
                print(e)

    '''
    检查常用命令： 
    jstack ---检查java进程
    
    
    '''


    def put(self, request,args=None):
        try:
            id = request.GET.get("ID")
            hostname = request.GET.get('h_hostname') #服务器名称
            IP = request.GET.get('h_IP')  #服务器IP地址
            group = request.GET.get('h_group')  #服务器所属分组
            username = request.GET.get('h_username')   #服务器ssh登录账号
            password = request.GET.get('h_password')   #服务器ssh登录密码
            keyfile = request.GET.get('keyfile')   # 服务器的key file
            #LoginMethod = request.GET.get('h_loginmethod')  # 登录服务器的方式

        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                ServerConf.objects.filter(id=id).update(
                    HostName=hostname,
                    IP=IP,
                    Group=group,
                    Username=username,
                    Password=password,
                    KeyFile=keyfile
                )
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)