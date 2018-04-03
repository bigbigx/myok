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
    AssetRoom,
    AssetArea
)

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')
conf = util.conf_path()

'''
物理资产信息，针对机房内的硬件信息，含物理机、防火墙、网络交换机、网络路由器等

'''
class assets(baseview.BaseView):
    '''
    获取资产清单
    '''
    def get(self, request, args=None):
        try:
            room_all = AssetRoom.objects.all()
            room_list=[]
            area_list=[]
            for i in room_all:
                room_list.append(i.room_remark)

            area_all = AssetArea.objects.filter(asset_room_id='R002').all()
            for i in area_all:
                area_list.append(i.area_name)

            data = {'room_list': room_list,'area_list': area_list}
            data = json.dumps(data)
            # 获取到区域信息
            return Response(data)
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
    '''
    创建资产
    '''

    def put(self, request, args=None):
        print(args)
        # 获取
        if args == 'cabinet':  ##  获取机柜信息
            try:

                computer_room = request.GET.get('room')
                id = request.GET.get('id')
            except KeyError as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    pass
                except Exception as e:
                    print(e)
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
                AssetRoom.object.filter(id=id).first()
            except KeyError as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                try:
                    pass

                except Exception as e:
                    print(e)

        # 获取机房的区域信息,选择了机房后，即从后端获取到区域、设备类型等信息给到用户选择
        elif args == 'room':
            try:
                room_name = request.GET.get("room_name")
                room_all = AssetRoom.object.all()
                room = AssetRoom.object.filter(room_name=room_name).first()
                area_list = AssetArea.object.filter(asset_room_id=room.room_id).all()
                data ={'room_list': room_all, 'area_list': area_list}
                # 获取到区域信息
                return Response(data=data,status=200)
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
        else:
            print("Nothing")


    '''
    编辑资产
    '''
    def post(self, request,args=None):

        pass


    '''
    删除资产
    '''
    def  delete(self, request,args=None):
        pass
