# -*- coding=utf-8 -*-
import logging
import json
from libs import send_email
from libs import baseview
from libs import call_inception
from libs import util
from libs import conn_sqlite
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    ServerInfo,
    ServerConf
)
from django.core.cache import cache

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

class host(baseview.BaseView):
    '''
    获取服务器清单
    '''
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
    创建服务器
    '''
    def post(self, request, args=None):
        try:
            hostname = request.GET.get('h_hostname') #服务器名称
            IP = request.GET.get('h_IP')  #服务器IP地址
            group = request.GET.get('h_group')  #服务器所属分组
            username = request.user.username   #服务器ssh登录账号
            password = request.GET.get('h_password')   #服务器ssh登录密码
            keyfile = request.GET.get('keyfile')   # 服务器的key file
            LoginMethod = request.GET.get('h_loginmethod')  # 登录服务器的方式

        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                ServerConf.objects.get_or_create(
                    HostName=hostname,
                    IP=IP,
                    Group=group,
                    Username=username,
                    Password=password,
                    KeyFile=keyfile,
                    LoginMethod=LoginMethod
                    )
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)


    '''
    编辑服务器内容,修改IP、主机名、或者描述、账号、密码等种种信息
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


    '''
    删除服务器
    '''
    def  delete(self, request,args=None):
        try:
            hostname = request.GET.get('h_hostname')  # 服务器名称
            IP = request.GET.get('h_IP')  # 服务器IP地址
            group = request.GET.get('h_group')  # 服务器所属分组
            username = request.GET.get('h_username')  # 服务器ssh登录账号
            password = request.GET.get('h_password')  # 服务器ssh登录密码
            keyfile = request.GET.get('keyfile')  # 服务器的key file
            LoginMethod = request.GET.get('h_loginmethod')  # 登录服务器的方式

        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                pass


            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

