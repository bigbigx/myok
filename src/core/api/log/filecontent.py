import time
import logging
from libs import util
import json
from libs import baseview
from django.forms.models import model_to_dict
from django.db.models import Count
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    ServerInfo,
    ServerConf,
    FileContent,
    AssetAreaList,
    YunEcsObj,
    YunRdsObj,
    Account
)
from libs.serializers import (
    Cabinet,
    UserINFO,
    FileContentSeri
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
                    ''' % username
                )[start:end]
                data = util.ser(info)
                return Response({'page': pagenumber, 'data': data})
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    def put(self, request, args=None):
        '''
        init:  初始化获取机房和云机器的清单、

        '''

        if args == 'init':
            print('init')
            try:
                area_list = []
                file_list = []
                info = AssetAreaList.objects.all()
                _serializers = Cabinet(info, many=True)
                user = Account.objects.all()
                user_serializers = UserINFO(user, many=True)

                tmp = FileContent.objects.all()
                for item in tmp:
                    tmp = {'file_title':item.file_title,'file_path': item.file_path,'public_server_ip':item.public_server_ip,'server_hostname':item.server_hostname,'private_server_ip':item.private_server_ip, 'file_type': item.file_type, 'file_remark': item.file_remark,'region_name':item.region_name, 'room_name':item.room_name}
                # filecontent_serializers = FileContentSeri(tmp, many=True)
                    file_list.append(tmp)
                print(file_list)
                return Response({'area':_serializers.data, 'user':user_serializers.data,'file_list': file_list})
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(500)

        elif args == 'instance':
            print('instance')
            try:
                area_name = request.data['area_name']
                room_name = request.data['room_name']
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(500)
            else:

                try:
                    ecs_name = []
                    obj = AssetAreaList.objects.filter(area_name=area_name, room_name=room_name).first()
                    ecs = YunEcsObj.objects.filter(RegionId=obj.area_id, Room_id=obj.room_id).all()
                    for item in ecs:
                        tmp = {'name': item.InstanceName, 'privateip': item.InnerIpAddress , 'publicip': item.PublicIpAddress,'status': item.Status}
                        ecs_name.append(tmp)
                    print(ecs_name)
                    return Response(ecs_name)

                except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(500)

    def post(self, request, args: str = None):
        print('post')
        try:
            room_name = request.data['room_name']
            area_name = request.data['area_name']
            publicip = request.data['publicip']
            privateip = request.data['privateip']
            server_instance_name = request.data['server_name']
            server_status = request.data['server_status']
            file_path = request.data['file_path']
            file_remark = request.data['file_remark']
            file_owner = request.data['file_owner']
            file_title = request.data['file_title']
            file_type = request.data['file_type']
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(500)
        else:
            try:
                FileContent.objects.get_or_create(
                    private_server_ip=privateip,
                    public_server_ip=publicip,
                    server_hostname=server_instance_name,
                    region_name=area_name,
                    room_name=room_name,
                    server_status=server_status,
                    pg_id='',
                    keyword='',
                    file_title=file_title,
                    file_type=file_type,
                    file_path=file_path,
                    file_remark=file_remark
                )


                return Response('已创建文件')

            except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(500)