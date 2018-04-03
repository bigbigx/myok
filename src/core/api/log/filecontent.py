import time
import logging
from libs import util
from libs import baseview
from django.db.models import Count
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    ServerInfo,
    ServerConf,
    FileContent
)

conf = util.conf_path()
addr_ip = conf.ipaddress
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')


class filecontent(baseview.Approverpermissions):
    '''
    获取文件或者日志的清单
    '''

    def get(self, request, args=None):
        try:
            username = request.GET.get('user')
            page = int(request.GET.get('page'))
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            ret_info = '<h1> 访问服务器异常</h1>'
            return HttpResponse(ret_info)
        else:
            try:
                pagenumber = FileContent.objects.filter(assigned=username).aggregate(alter_number=Count('id'))
                start = (int(page) - 1) * 20
                end = int(page) * 20
                info = FileContent.objects.raw(
                    '''
                    select core_sqlorder.*,core_databaselist.connection_name, \
                    core_databaselist.computer_room from FileContent \
                    INNER JOIN core_databaselist on \
                    core_sqlorder.bundle_id = core_databaselist.id where core_sqlorder.assigned = '%s'\
                    ORDER BY core_sqlorder.id desc
                    '''%username
                )[start:end]
                data = util.ser(info)
                return Response({'page': pagenumber, 'data': data})
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    def put(self, request, args=None):

        '''
         查看实时日志  查看整个文件内容
        '''
        try:

            type = int(request.GET.get('type'))
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            ret_info = '<h1> 访问服务器异常</h1>'
            return HttpResponse(ret_info)
        else:
            if type == 0:  # 查看实时日志
                pass
            elif type == 1:  # 查看整个文件内容
                pass


def post(self, request, args: str = None):
        pass
