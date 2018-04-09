'''
serializers 
'''
from rest_framework import serializers
from core.models import Usermessage
from core.models import DatabaseList
from core.models import SqlDictionary
from core.models import SqlRecord
from core.models import Account
from core.models import AssetAreaList
from core.models import FileContent



class MessagesUser(serializers.HyperlinkedModelSerializer):
    '''
    站内信列表serializers
    '''
    class Meta:
        model = Usermessage
        fields = ('title', 'time')


class UserINFO(serializers.HyperlinkedModelSerializer):
    '''
    平台用户信息列表serializers
    '''
    class Meta:
        model = Account
        fields = ('username', 'group', 'department', 'email')

class FileContentSeri(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileContent
        fields = (
            'private_server_ip', 'public_server_ip', 'server_hostname', 'region_name',
            'room_name', 'server_status', 'pg_id', 'file_title' , 'file_type', 'file_path', 'file_remark' , 'keyword'
            )


class SQLGeneratDic(serializers.HyperlinkedModelSerializer):
    '''
    数据库字典信息serializers
    '''
    class Meta:
        model = SqlDictionary
        fields = (
            'BaseName', 'TableName', 'Field', 'Type',
            'Null', 'Default', 'Extra', 'TableComment'
            )


class Sqllist(serializers.HyperlinkedModelSerializer):
    '''
    数据库连接信息serializers
    '''
    class Meta:
        model = DatabaseList
        fields = ('id', 'connection_name', 'ip', 'computer_room', 'password', 'port', 'username')

class Cabinet(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AssetAreaList
        fields = ('id', 'room_id', 'room_name', 'area_name')


class Area(serializers.HyperlinkedModelSerializer):
    '''
    SQL提交及表结构修改页面数据库连接信息返回serializers
    '''
    class Meta:
        model = DatabaseList
        fields = ('id', 'connection_name', 'ip', 'computer_room')

class Record(serializers.HyperlinkedModelSerializer):
    '''
    执行工单的详细信息serializers
    '''
    class Meta:
        model = SqlRecord
        fields = (
            'sql', 'state', 'error', 'affectrow',
            'sequence', 'area', 'name', 'base', 'rollbackid'
            )


class Getdingding(serializers.HyperlinkedModelSerializer):
    '''
    dingding webhook serializers
    '''
    class Meta:
        model = DatabaseList
        fields = ('id', 'before', 'after', 'url')
