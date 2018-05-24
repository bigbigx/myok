# -*- coding=utf-8 -*-

import logging
# import json

from libs import baseview
from libs import util
from rest_framework.response import Response
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

from django.http import HttpResponse
from core.models import (
    Config
)

class config(baseview.Approverpermissions):

    '''
    配置相关信息
    '''
    def get(self, request, args=None):
        try:
            type = request.GET.get('type')
            flow = request.GET.get('flow')
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                info = Config.objects.filter(type=type,flow_or_not=flow).all()
                data = util.ser(info)
                print(data)
                return Response(data)
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)



    def put(self, request, args=None):
        try:
            type = request.data['type']
            # basename = str(request.data['basename'])
            execute_man = 'dba'
            # cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except KeyError as e:
            #print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            if args == 'forbbiden': # 调整配置数据的状态值为禁止
                pass

            elif args == 'used':# 调整配置数据的状态值为启用
                pass

            elif args == '':
                pass

            else:

                pass


    def post(self, request, args: str = None):
        try:
            dataid = json.loads(request.data['id'])
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:

            pass


    # 删除配置
    def delelte(self, request, args=None):
        try:
            dataid = request.data['id']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            pass