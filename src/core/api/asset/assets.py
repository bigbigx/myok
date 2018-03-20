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
    ServerConf,
    AssetBasic
)

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

'''
物理资产信息，针对机房内的硬件信息，含物理机、防火墙、网络交换机、网络路由器等

'''
class assets(baseview.BaseView):
    '''
    获取资产清单
    '''
    def get(self, request, args=None):
        try:
            page = request.GET.get('page')
            #username = request.GET.get('username')

        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                asset_list={}

                return Response(res=asset_list,status=200)

            except Exception as e:
                print(e)
    '''
    创建资产
    '''

    def post(self, request, args=None):
        # 添加新的资产
        if args == 'add':
            try:
                asset_name = request.GET.get('name') #资产名称
                position = request.GET.get('position')  #机房
                descript = request.GET.get('descript')  #描述
                CPU = request.GET.get('CPU')   #CPU型号
                MEM = request.GET.get('MEM')   # 内存大小
                flatform = request.GET.get('MEM')   #  平台
                os = request.GET.get('MEM')  #操作系统
                InBankWidth = request.GET.get('InBankWidth')
                OutBankWidth = request.GET.get('OutBankWidth')
                AssetBasic.object.filter(id=id).first()
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    pass

                except Exception as e:
                    print(e)

        # 获取机房的区域信息
        elif args == "area":
            try:
                asset_name = request.GET.get('name') #资产名称
                room = request.GET.get('room')  #机房

                AssetBasic.object.filter(id=id).first()
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    pass

                except Exception as e:
                    print(e)



    '''
    编辑资产
    '''
    def put(self, request,args=None):

        pass


    '''
    删除资产
    '''
    def  delete(self, request,args=None):
        pass
