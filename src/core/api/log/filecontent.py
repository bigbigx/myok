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
    Account,
    AccountGroup
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
    我的文件 菜单 进入方法： 获取某个用户下的其所有文件
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
                data = []
                start = (int(page) - 1) * 20
                end = int(page) * 20

                pagenumber = FileContent.objects.aggregate(alter_number=Count('id'))
                workgroup_name= Account.objects.filter(username=username).first()
                if workgroup_name is not None:

                    account_group = AccountGroup.objects.filter(GroupID=workgroup_name.workgroup_id).first()
                    print(account_group)
                    # FileContent.objects.filter(assigned=username).aggregate(alter_number=Count('id'))
                    info = FileContent.objects.filter(file_owner=account_group.GroupName).all()
                    print(info)
                    if info is not None:  # 如果查询有结果，那么执行
                        for item in info:
                            tmp = {'file_title': item.file_title, 'file_path': item.file_path,
                                   'file_owner': item.file_owner, 'public_server_ip': item.public_server_ip,
                                   'server_hostname': item.server_hostname, 'private_server_ip': item.private_server_ip,
                                   'file_type': item.file_type, 'file_remark': item.file_remark,
                                   'region_name': item.region_name, 'room_name': item.room_name,
                                   'full_file_status':item.full_file_status,
                                   'keyword': item.keyword,
                                   'visit_user':item.visit_user,'visit_way':item.visit_way}
                            # filecontent_serializers = FileContentSeri(tmp, many=True)
                            data.append(tmp)
                    # data = util.ser(info)
                return Response({'page': pagenumber, 'data': data})
            except Exception as e:
                print(e)
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
                group_list = []
                info = AssetAreaList.objects.all()
                _serializers = Cabinet(info, many=True)
                user = Account.objects.all()
                user_serializers = UserINFO(user, many=True)
                group_info = AccountGroup.objects.filter(status=1).all()
                tmp = FileContent.objects.all()
                for item in tmp:
                    tmp = {'id': item.id,'full_file_status': item.full_file_status, 'file_title': item.file_title,'file_path': item.file_path, 'file_owner': item.file_owner,'public_server_ip':item.public_server_ip,'server_hostname':item.server_hostname,'private_server_ip':item.private_server_ip, 'file_type': item.file_type, 'file_remark': item.file_remark,'region_name':item.region_name, 'room_name':item.room_name}
                    file_list.append(tmp)
                # print(file_list)
                for group in group_info:
                    group_tmp = {'name': group.GroupName, 'ID': group.GroupID}
                    group_list.append(group_tmp)
                return Response({'area': _serializers.data, 'user': user_serializers.data, 'file_list': file_list, 'group': group_list})
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

        elif args == 'save_status':
            try:
                full_file_status = request.data['full_file_status']
                file_id = request.data['file_id']
                print(full_file_status)
                print(file_id)
            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                # return HttpResponse({'title': '失败', 'data': 500})
                return HttpResponse(500)
            else:
                try:

                    if file_id != '':
                        FileContent.objects.filter(id=file_id).update(
                            full_file_status=full_file_status
                        )
                        # return Response('修改成功！ 目前是否启用：%s ' % (str(file_id), str(full_file_status)))
                        return Response('修改成功！')
                    else:
                        return Response('没有找到匹配的文件ID')
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
                    file_remark=file_remark,
                    file_owner=file_owner
                )


                return Response('已创建文件')

            except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(500)

    def delete(self, request, args: str = None):
        try:
            FileContent.objects.filter(file_title=args).delete()
            return Response('数据库信息已删除!')
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
