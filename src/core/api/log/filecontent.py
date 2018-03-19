import time
import logging
from libs import util
from libs import baseview
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    ServerInfo,
    ServerConf
)

conf = util.conf_path()
addr_ip = conf.ipaddress
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

class filecontent(baseview.Approverpermissions):
    '''
    文件内容的实时显示
    '''
    def get(self, request, args=None):
        try:

            type = int(request.GET.get('type'))
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            ret_info = '<h1> 访问服务器异常</h1>'
            return HttpResponse(ret_info)
        else:
            pass



    def put(self, request, args=None):
        try:

            type = int(request.GET.get('type'))
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            ret_info = '<h1> 访问服务器异常</h1>'
            return HttpResponse(ret_info)
        else:
            pass



    def post(self, request, args: str = None):
            pass
