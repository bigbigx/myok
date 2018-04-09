# -*- coding=utf-8 -*-
import logging
import json
import datetime
from libs import send_email
from libs import baseview
from libs import call_inception
from libs import util
from libs import spider
from core.api.asset.assetobj import assetobj
from libs import conn_sqlite
from libs import con_database
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    ServerInfo,
    ServerConf,
    AssetRoom,
    AssetArea,
    YunRdsObj,
    YunEcsObj,
    AssetChangeHistory
)

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')
conf = util.conf_path()

'''
云环境资产信息

'''


class yunassets(baseview.BaseView):
    '''
    获取云资产清单(数据库里面的清单)，包括RDS,ECS,等等
    '''

    def get(self, request, args=None):
        try:
            sql_ecs ="select *  from core_yunecsobj"

            with con_database.SQLgo(ip='101.236.41.66', password='wang', user='wang', port=3306,
                                    db='Yearning') as f:
                ecs_dataset = f.search(sql=sql_ecs)

            sql_rds = "select *  from core_yunrdsobj"

            with con_database.SQLgo(ip='101.236.41.66', password='wang', user='wang', port=3306,
                                        db='Yearning') as k:
                rds_dataset = k.search(sql=sql_rds)
                # print(dataset)
            return Response({'ecs_data': ecs_dataset, 'rds_data': rds_dataset})
            # return Response(rds_dataset)
            #     return Response([{'ecs': ecs_dataset}])
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)

    def put(self, request, args=None):
        # 获取阿里云没有中和现资产清单不一样的信息，含未添加，已删除，以及配置信息变动等等信息，
        if args == 'showdiff':
            print('showdiff')
            try:
                cur_time = datetime.datetime.now()
                data_ecs = []
                data_rds = []
                tmp = {}
                tmp = [{'type': '', 'instance_name': '', 'instance_id': '', 'msg': ''}]
                # result = {'type': '', 'instanceid': '', 'diff': '', 'checktime': ''}
                rds_result_list = spider.yunSpider().RDS()
                ecs_result_list = spider.yunSpider().ECS()
                old_ecs_result_list = []
                old_rds_result_list = []
                try:
                    sql = "select *  from core_yunecsobj"

                    with con_database.SQLgo(ip='101.236.41.66', password='wang', user='wang', port=3306,
                                            db='Yearning') as f:
                        old_ecs_result_list = f.search(sql=sql)
                        print(old_ecs_result_list)

                        print(len(old_ecs_result_list))
                        print(old_ecs_result_list['len'])
                except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                try:
                    sql = "select *  from core_yunrdsobj"

                    with con_database.SQLgo(ip='101.236.41.66', password='wang', user='wang', port=3306,
                                            db='Yearning') as f:
                        old_rds_result_list = f.search(sql=sql)
                        print(old_rds_result_list)
                        print(old_rds_result_list['len'])
                except Exception as e:
                    print(e)
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')

                if old_ecs_result_list['len'] == 0:
                    data_ecs = data_ecs + ecs_result_list
                else:

                    for instance_ecs in ecs_result_list:  ### ecs检查
                        for instance_ecs_old in old_ecs_result_list:
                            # if instance_ecs_old['InstanceId'] == '':  #  数据库内容为空
                            # 检查各种细项
                            if instance_ecs_old['InstanceId'] == instance_ecs['InstanceId']:
                                result = {}
                                if instance_ecs_old['InnerIpAddress'] != instance_ecs['InnerIpAddress']: result[
                                    'InnerIpAddress'] = instance_ecs['InnerIpAddress']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['ImageId'] = \
                                instance_ecs['ImageId']
                                if instance_ecs_old['InstanceTypeFamily'] != instance_ecs['InstanceTypeFamily']: result[
                                    'InstanceTypeFamily'] = instance_ecs['InstanceTypeFamily']
                                if instance_ecs_old['VlanId'] != instance_ecs['VlanId']: result['VlanId'] = \
                                instance_ecs[
                                    'VlanId']
                                if instance_ecs_old['EipAddress'] != instance_ecs['EipAddress']: result['EipAddress'] = \
                                    instance_ecs['EipAddress']
                                if instance_ecs_old['InternetMaxBandwidthIn'] != instance_ecs['InternetMaxBandwidthIn']: \
                                        result['InternetMaxBandwidthIn'] = instance_ecs['InternetMaxBandwidthIn']  ###
                                if instance_ecs_old['ZoneId'] != instance_ecs['ZoneId']: result['ZoneId'] = \
                                instance_ecs[
                                    'ZoneId']
                                if instance_ecs_old['InternetChargeType'] != instance_ecs['InternetChargeType']: result[
                                    'InternetChargeType'] = instance_ecs['InternetChargeType']
                                if instance_ecs_old['SpotStrategy'] != instance_ecs['SpotStrategy']: result[
                                    'SpotStrategy'] = instance_ecs['SpotStrategy']
                                if instance_ecs_old['StoppedMode'] != instance_ecs['StoppedMode']: result[
                                    'StoppedMode'] = \
                                    instance_ecs['StoppedMode']
                                if instance_ecs_old['SerialNumber'] != instance_ecs['SerialNumber']: result[
                                    'SerialNumber'] = instance_ecs['SerialNumber']
                                if instance_ecs_old['IoOptimized'] != instance_ecs['IoOptimized']: result['IoOptimized'] = \
                                    instance_ecs['IoOptimized']
                                if instance_ecs_old['Memory'] != instance_ecs['Memory']: result['Memory'] = \
                                instance_ecs['Memory']
                                if instance_ecs_old['Cpu'] != instance_ecs['Cpu']: result['Cpu'] = instance_ecs['Cpu']
                                if instance_ecs_old['VpcAttributes'] != instance_ecs['VpcAttributes']: result[
                                    'VpcAttributes'] = instance_ecs['VpcAttributes']
                                if instance_ecs_old['InternetMaxBandwidthOut'] != instance_ecs['InternetMaxBandwidthOut']: \
                                        result['InternetMaxBandwidthOut'] = instance_ecs['InternetMaxBandwidthOut']
                                if instance_ecs_old['DeviceAvailable'] != instance_ecs['DeviceAvailable']: result['DeviceAvailable'] = instance_ecs['DeviceAvailable']
                                if instance_ecs_old['SecurityGroupIds'] != instance_ecs['SecurityGroupIds']: result['SecurityGroupIds'] = instance_ecs['SecurityGroupIds']
                                if instance_ecs_old['SaleCycle'] != instance_ecs['SaleCycle']: result['SaleCycle'] = \
                                    instance_ecs['SaleCycle']
                                if instance_ecs_old['SpotPriceLimit'] != instance_ecs['SpotPriceLimit']: result[
                                    'SpotPriceLimit'] = instance_ecs['SpotPriceLimit']
                                if instance_ecs_old['AutoReleaseTime'] != instance_ecs['AutoReleaseTime']: result[
                                    'AutoReleaseTime'] = instance_ecs['AutoReleaseTime']
                                if instance_ecs_old['StartTime'] != instance_ecs['StartTime']: result['StartTime'] = \
                                    instance_ecs['StartTime']
                                if instance_ecs_old['InstanceName'] != instance_ecs['InstanceName']: result[
                                    'InstanceName'] = instance_ecs['InstanceName']
                                if instance_ecs_old['Description'] != instance_ecs['Description']: result[
                                    'Description'] = \
                                    instance_ecs['Description']
                                if instance_ecs_old['ResourceGroupId'] != instance_ecs['ResourceGroupId']: result[
                                    'ResourceGroupId'] = instance_ecs['ResourceGroupId']
                                if instance_ecs_old['OSType'] != instance_ecs['OSType']: result['OSType'] = \
                                instance_ecs[
                                    'OSType']
                                if instance_ecs_old['OSName'] != instance_ecs['OSName']: result['OSName'] = \
                                instance_ecs[
                                    'OSName']
                                if instance_ecs_old['InstanceNetworkType'] != instance_ecs['InstanceNetworkType']:
                                    result['InstanceNetworkType'] = instance_ecs['InstanceNetworkType']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['PublicIpAddress'] = \
                                    instance_ecs['PublicIpAddress']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['HostName'] = \
                                    instance_ecs['HostName']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['InstanceType'] = \
                                    instance_ecs['InstanceType']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['CreationTime'] = \
                                    instance_ecs['CreationTime']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['Status'] = \
                                instance_ecs[
                                    'Status']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['ClusterId'] = \
                                    instance_ecs['ClusterId']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['Recyclable'] = \
                                    instance_ecs['Recyclable']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['RegionId'] = \
                                    instance_ecs['RegionId']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['GPUSpec'] = \
                                instance_ecs[
                                    'GPUSpec']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['OperationLocks'] = \
                                    instance_ecs['OperationLocks']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result[
                                    'InstanceChargeType'] = \
                                    instance_ecs['InstanceChargeType']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['GPUAmount'] = \
                                    instance_ecs['GPUAmount']
                                if instance_ecs_old['ImageId'] != instance_ecs['ImageId']: result['xpiredTime'] = \
                                    instance_ecs['xpiredTime']
                                # if instance_ecs_old['ImageId'] != instance_ecs['ImageId']:instance_ecs.append(instance_rds['InstanceId'])
                                data_ecs.append(result)

                            else:
                                # if
                                break
                if old_rds_result_list['len'] == 0:
                    data_rds = data_rds + rds_result_list
                else:
                    for instance_rds in rds_result_list:  ### RDS检查
                        for instance_rds_old in old_rds_result_list:
                            # 检查各种细项
                            if instance_rds_old['DBInstanceId'] == instance_rds['DBInstanceId']:
                                result_rds = {}
                                if instance_ecs_old['InnerIpAddress'] != instance_ecs['InnerIpAddress']: result[
                                    'InnerIpAddress'] = instance_ecs['InnerIpAddress']
                                if instance_ecs_old['LockMode'] != instance_ecs['LockMode']: result['LockMode'] = \
                                    instance_ecs['LockMode']
                                if instance_ecs_old['DBInstanceNetType'] != instance_ecs['DBInstanceNetType']: result[
                                    'DBInstanceNetType'] = instance_ecs['DBInstanceNetType']
                                if instance_ecs_old['DBInstanceClass'] != instance_ecs['DBInstanceClass']: result[
                                    'DBInstanceClass'] = instance_ecs['DBInstanceClass']
                                if instance_ecs_old['ResourceGroupId'] != instance_ecs['ResourceGroupId']: result[
                                    'ResourceGroupId'] = instance_ecs['ResourceGroupId']
                                if instance_ecs_old['VpcCloudInstanceId'] != instance_ecs['VpcCloudInstanceId']: result[
                                    'VpcCloudInstanceId'] = instance_ecs['VpcCloudInstanceId']
                                if instance_ecs_old['ZoneId'] != instance_ecs['ZoneId']: result['ZoneId'] = \
                                instance_ecs[
                                    'ZoneId']
                                if instance_ecs_old['ReadOnlyDBInstanceIds'] != instance_ecs['ReadOnlyDBInstanceIds']: \
                                        result['ReadOnlyDBInstanceIds'] = instance_ecs['ReadOnlyDBInstanceIds']
                                if instance_ecs_old['InstanceNetworkType'] != instance_ecs['InstanceNetworkType']:
                                        result['InstanceNetworkType'] = instance_ecs['InstanceNetworkType']
                                if instance_ecs_old['DBInstanceDescription'] != instance_ecs['DBInstanceDescription']: \
                                        result['DBInstanceDescription'] = instance_ecs['DBInstanceDescription']
                                if instance_ecs_old['ConnectionMode'] != instance_ecs['ConnectionMode']: result[
                                    'ConnectionMode'] = instance_ecs['ConnectionMode']
                                if instance_ecs_old['Engine'] != instance_ecs['Engine']: result['Engine'] = \
                                instance_ecs[
                                    'Engine']
                                if instance_ecs_old['MutriORsignle'] != instance_ecs['MutriORsignle']: result[
                                    'MutriORsignle'] = instance_ecs['MutriORsignle']
                                if instance_ecs_old['InsId'] != instance_ecs['InsId']: result['InsId'] = instance_ecs[
                                    'InsId']
                                if instance_ecs_old['ExpireTime'] != instance_ecs['ExpireTime']: result['ExpireTime'] = \
                                    instance_ecs['ExpireTime']
                                if instance_ecs_old['CreateTime'] != instance_ecs['CreateTime']: result['CreateTime'] = \
                                    instance_ecs['CreateTime']
                                if instance_ecs_old['DBInstanceType'] != instance_ecs['DBInstanceType']: result[
                                    'DBInstanceType'] = instance_ecs['DBInstanceType']
                                if instance_ecs_old['RegionId'] != instance_ecs['RegionId']: result['RegionId'] = \
                                    instance_ecs['RegionId']
                                if instance_ecs_old['EngineVersion'] != instance_ecs['EngineVersion']: result[
                                    'EngineVersion'] = instance_ecs['EngineVersion']
                                if instance_ecs_old['LockReason'] != instance_ecs['LockReason']: result['LockReason'] = \
                                    instance_ecs['LockReason']
                                if instance_ecs_old['DBInstanceStatus'] != instance_ecs['DBInstanceStatus']: result[
                                    'DBInstanceStatus'] = instance_ecs['DBInstanceStatus']
                                if instance_ecs_old['PayType'] != instance_ecs['PayType']: result['PayType'] = \
                                instance_ecs[
                                    'PayType']
                                data_rds.append(result)
                            else:
                                break

                return Response({'diff_detail': {'ecs': data_ecs, 'rds': data_rds}})

            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(500)


        elif args == 'savediff':
            print("Nothing")


    '''
    添加云资产
    '''


    def post(self, request, args=None):
        print('post')
        try:
            user = request.data['user']
            ecs_data = json.loads(request.data['ecs_data'])  #  将字符串转化为dict
            # ecs_data = request.data['ecs_data']
            rds_data = json.loads(request.data['rds_data'])
            # rds_data = request.data['rds_data']
            print(ecs_data)
            print(rds_data)


        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                cur_time = datetime.datetime.now()
                for ecs in ecs_data:
                    YunEcsObj.objects.get_or_create(
                        InnerIpAddress=ecs['InnerIpAddress'],
                        ImageId=ecs['ImageId'],
                        InstanceTypeFamily=ecs['InstanceTypeFamily'],
                        VlanId=ecs['VlanId'],
                        InstanceId=ecs['InstanceId'],
                        EipAddress=ecs['EipAddress'],
                        InternetMaxBandwidthIn=ecs['InternetMaxBandwidthIn'],
                        ZoneId=ecs['ZoneId'],
                        InternetChargeType=ecs['InternetChargeType'],
                        SpotStrategy=ecs['SpotStrategy'],
                        StoppedMode=ecs['StoppedMode'],
                        SerialNumber=ecs['SerialNumber'],
                        IoOptimized=ecs['IoOptimized'],
                        Memory=ecs['Memory'],
                        Cpu=ecs['Cpu'],
                        VpcAttributes=ecs['VpcAttributes'],
                        InternetMaxBandwidthOut=ecs['InternetMaxBandwidthOut'],
                        DeviceAvailable=ecs['DeviceAvailable'],
                        SecurityGroupIds=ecs['SecurityGroupIds'],
                        SaleCycle=ecs['SaleCycle'],
                        SpotPriceLimit=ecs['SpotPriceLimit'],
                        AutoReleaseTime=ecs['AutoReleaseTime'],
                        StartTime=ecs['StartTime'],
                        InstanceName=ecs['InstanceName'],
                        Description=ecs['Description'],
                        ResourceGroupId=ecs['ResourceGroupId'],
                        OSType=ecs['OSType'],
                        OSName=ecs['OSName'],
                        InstanceNetworkType=ecs['InstanceNetworkType'],
                        PublicIpAddress=ecs['PublicIpAddress'],
                        HostName=ecs['HostName'],
                        InstanceType=ecs['InstanceType'],
                        CreationTime=ecs['CreationTime'],
                        Status=ecs['Status'],
                        ClusterId=ecs['ClusterId'],
                        Recyclable=ecs['Recyclable'],
                        RegionId=ecs['RegionId'],
                        GPUSpec=ecs['GPUSpec'],
                        OperationLocks=ecs['OperationLocks'],
                        InstanceChargeType=ecs['InstanceChargeType'],
                        GPUAmount=ecs['GPUAmount'],
                        xpiredTime=ecs['xpiredTime']
                    )
                for rds in rds_data:
                    YunRdsObj.objects.get_or_create(
                        LockMode=rds['LockMode'],
                        DBInstanceNetType=rds['DBInstanceNetType'],
                        DBInstanceClass=rds['DBInstanceClass'],
                        ResourceGroupId=rds['ResourceGroupId'],
                        DBInstanceId=rds['DBInstanceId'],
                        VpcCloudInstanceId=rds['VpcCloudInstanceId'],
                        ZoneId=rds['ZoneId'],
                        ReadOnlyDBInstanceIds=rds['ReadOnlyDBInstanceIds'],
                        InstanceNetworkType=rds['InstanceNetworkType'],
                        DBInstanceDescription=rds['DBInstanceDescription'],
                        ConnectionMode=rds['ConnectionMode'],
                        Engine=rds['Engine'],
                        MutriORsignle=rds['MutriORsignle'],
                        InsId=rds['InsId'],
                        ExpireTime=rds['ExpireTime'],
                        CreateTime=rds['CreateTime'],
                        DBInstanceType=rds['DBInstanceType'],
                        RegionId=rds['RegionId'],
                        EngineVersion=rds['EngineVersion'],
                        LockReason=rds['LockReason'],
                        DBInstanceStatus=rds['DBInstanceStatus'],
                        PayType=rds['PayType']
                    )

                # 加入到资产操作记录表里
                content = {'ecs': ecs_data, 'rds': rds_data}
                record = [{'cur_time': cur_time, 'content': content, 'person': user}]
                AssetChangeHistory.objects.get_or_create(
                    time=cur_time,
                    content=content,
                    person=user
                )
                return Response({'data': record, 'status': 200})

            except Exception as e:
                print(e)
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)


    '''
    删除资产
    '''


    def delete(self, request, args=None):
        pass
