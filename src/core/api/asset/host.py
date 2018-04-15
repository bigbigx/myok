# -*- coding=utf-8 -*-
import logging
import paramiko

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
    ServerConf,
    AccountGroup,
    Account,
    HostUserPwd
)
from django.core.cache import cache

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

class host(baseview.BaseView):
    '''
    获取服务器用户密码清单
    '''
    def get(self, request, args=None):
        print(args)
        if args == "myhost":
            print('myhost')
            try:
                page = request.GET.get('page')
                username = request.GET.get('user')
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    data = []
                    print(username)
                    account = Account.objects.filter(username=username).first()
                    group_id = account.workgroup_id
                    print(group_id)
                    if group_id != '':
                        group = AccountGroup.objects.filter(GroupID=group_id).first()
                        print(group)
                        host_user = HostUserPwd.objects.filter(workgroup_id=group_id).all()
                        for item in host_user:
                            tmp = {'username':  item.user_name, 'remark': item.remark, 'publicip': item.public_IP, 'privateip': item.private_IP}
                            data.append(tmp)

                    print('ddd')
                    print(data)
                    return Response(data)

                except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse({'data': f'{e.__class__.__name__}: {e}', 'status': 202})
        else:
            print('else')
            try:
                pass
                # page = request.GET.get('page')
                # username = request.GET.get('username')
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    data = []
                    data1 = []
                    host_user_list = HostUserPwd.objects.all()
                    host_user_list_distinct = HostUserPwd.objects.values('public_IP','private_IP').distinct()
                    print(host_user_list_distinct)
                    for item in host_user_list:
                        workgroup_id = item.workgroup_id
                        account = AccountGroup.objects.filter(GroupID=workgroup_id).first()
                        tmp ={'username': item.user_name, 'publicip': item.public_IP, 'privateip': item.private_IP, 'remark': item.remark, 'server_status': item.server_status, 'workgroup': account.GroupName}
                        data.append(tmp)

                    for item in host_user_list_distinct:
                        # tmp = {'username': item.user_name, 'publicip': item.public_IP, 'privateip': item.private_IP,
                        #        'remark': item.remark, 'server_status': item.server_status,
                        #        'workgroup': account.GroupName}
                        tmp = { 'publicip': item['public_IP'],'privateip': item['private_IP']}
                        data1.append(tmp)

                    return Response({'data':data, 'distinct_data': data1})
                except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)


    '''
    添加ssh 用户账号对象
    '''
    def post(self, request, args=None):
        try:
            publicip = request.data['publicip']
            privateip = request.data['privateip']
            ssh_user = request.data['ssh_user']
            ssh_pwd = request.data['ssh_pwd']
            remark = request.data['remark']

        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                if publicip != '':
                    user = HostUserPwd.objects.filter(public_IP=publicip,user_name=ssh_user).first()
                    # print(user)
                    if user is not None:
                        return Response('此IP下的用户已经存在，无须创建')
                if privateip != '':
                    user = HostUserPwd.objects.filter(private_IP=privateip,user_name=ssh_user).first()
                    # print(user)
                    if user is not None:
                        return Response('此IP下的用户已经存在，无须创建')
                HostUserPwd.objects.get_or_create(
                    public_IP=publicip,
                    private_IP=privateip,
                    mac_address='',
                    user_name=ssh_user,
                    password=util.mycode(ssh_pwd),
                    remark=remark,
                    type=2,  #普通用户
                    status=1  # 1启用状态
                    )
                data = []
                host_user_list = HostUserPwd.objects.all()
                for item in host_user_list:
                    tmp = {'username': item.user_name, 'publicip': item.public_IP, 'privateip': item.private_IP,
                           'remark': item.remark}
                    data.append(tmp)
                return Response({'msg':'创建SSH用户成功','data': data})
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)


    '''
    编辑服务器内容,修改IP、主机名、或者描述、账号、密码等种种信息
    '''
    def put(self, request, args=None):
        if args=="init":
            try:
                pass

                # id = request.GET.get("ID")
                # groupname = request.GET.get('h_hostname') #服务器名称
                # IP = request.GET.get('h_IP')  #服务器IP地址
                # group = request.GET.get('h_group')  #服务器所属分组
                # username = request.GET.get('h_username')   #服务器ssh登录账号
                # password = request.GET.get('h_password')   #服务器ssh登录密码
                # keyfile = request.GET.get('keyfile')   # 服务器的key file
                # #LoginMethod = request.GET.get('h_loginmethod')  # 登录服务器的方式

            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:

                    data = []
                    ssh_user_list = HostUserPwd.objects.all()
                    for item in ssh_user_list:
                        tmp = {'username': item.user_name,'userpwd': item.password,'public_ip': item.public_IP,'private_ip':item.private_IP}
                        data.append(item)

                    return Response(data)
                except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
        elif args=="test":
            try:
                publicip = request.data['publicip']
                privateip = request.data['privateip']
                ssh_user = request.data['ssh_user']
                ssh_pwd = request.data['ssh_pwd']

            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    if publicip == '' or publicip is None:  #  公网地址为空
                        return Response('测试ssh连接需要公网地址测试，此服务器没有公网IP')
                    else:

                        client = paramiko.SSHClient()
                        # client.load_host_keys('/home/root/.ssh/known_hosts') #支持用密钥认证代替密码验证,实际环境推荐使用密钥认证
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 设置自动添加和保存目标ssh服务器的ssh密钥
                        client.connect(publicip, username=ssh_user, password=ssh_pwd)  # 连接
                        # ssh_session = client.get_transport().open_session()  # 打开会话
                        client.close()
                        return Response({'data': 'ssh连接测试成功','status': 200})

                except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse({'data': f'{e.__class__.__name__}: {e}','status': 202})





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

