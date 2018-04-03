#!/usr/bin/env python
# coding=utf-8
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json
# from libs import con_database
import pymysql

# 参数传入
# accessKey = sys[0]
# accessSecret = sys[1]
# region = sys[2]

# 获得cn-qingdao ecs列表
class  yunSpider(object):
    # def __init__(self,accessKey,accessSecret,region):
    def __init__(self):
        # self.clt =client.AcsClient(accessKey, accessSecret, region)
        self.clt = client.AcsClient('LTAILcALtfLdPgoY', 'eAQUuNEBEFT0Eoa1N4FFMZ9R6v3PXY', 'cn-qingdao')
        self.result_new = []
        self.result_old = []


    def RDS(self):

        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        request.set_PageSize(100)  # 每页条数
        request.set_PageNumber(1)  # 第几页
        response = json.loads(self.clt.do_action_with_exception(request), encoding='utf-8')
        data = []
        for info in response.get('Items').get('DBInstance'):
            result ={}

            result['LockMode'] = info.get('LockMode')
            result['DBInstanceNetType'] = info.get('DBInstanceNetType')
            result['DBInstanceClass'] = info.get('DBInstanceClass')
            result['ResourceGroupId'] = info.get('ResourceGroupId')
            result['DBInstanceId'] = info.get('DBInstanceId')
            result['VpcCloudInstanceId'] = info.get('VpcCloudInstanceId')
            result['ZoneId'] = info.get('ZoneId')
            result['ReadOnlyDBInstanceIds'] = info.get('ReadOnlyDBInstanceIds')
            result['InstanceNetworkType'] = info.get('InstanceNetworkType')
            result['DBInstanceDescription'] = info.get('DBInstanceDescription')
            result['ConnectionMode'] = info.get('ConnectionMode')
            result['Engine'] = info.get('Engine')
            result['MutriORsignle'] = info.get('MutriORsignle')
            result['InsId'] = info.get('InsId')
            result['ExpireTime'] = info.get('ExpireTime')
            result['CreateTime'] = info.get('CreateTime')
            result['DBInstanceType'] = info.get('DBInstanceType')
            result['RegionId'] = info.get('RegionId')
            result['EngineVersion'] = info.get('EngineVersion')
            result['LockReason'] = info.get('LockReason')
            result['DBInstanceStatus'] = info.get('DBInstanceStatus')
            result['PayType'] = info.get('PayType')
            data.append(result)
        return data
            #
            # rds_no = info.get('DBInstanceId');
            # rds_name = info.get('DBInstanceDescription')
            # region = info.get('RegionId')
            # zone = info.get('ZoneId')
            # engine = info.get('Engine')
            # engineVersion = info.get('EngineVersion')
            # payType = info.get('PayType')
            # rdsNetType = info.get('DBInstanceNetType')
            # rdsClass = info.get('DBInstanceClass')
            # rdsStatus = info.get('DBInstanceStatus')
            # creteTime = info.get('CreateTime')
            # expireTime = info.get('ExpireTime')
            #
            # result = [{'rds_id': rds_no, 'rds_name': rds_name}]


    def ECS(self):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.set_PageSize(100)  # 每页条数
        request.set_PageNumber(1)  # 第几页
        # PageNumber, PageSize
        response = json.loads(self.clt.do_action_with_exception(request), encoding='utf-8')
        info_list = response.get('Instances').get('Instance')


        data=[]
        # 遍历获取到的结果
        for info in info_list:
            result = {}
            result['InnerIpAddress'] = info.get('InnerIpAddress')
            result['ImageId'] = info.get('ImageId')
            result['InstanceTypeFamily'] = info.get('InstanceTypeFamily')
            result['VlanId']= info.get('VlanId')
            result['InstanceId'] = info.get('InstanceId')
            result['EipAddress'] = info.get('EipAddress')
            result['InternetMaxBandwidthIn'] = info.get('InternetMaxBandwidthIn')
            result['ZoneId'] = info.get('ZoneId')
            result['InternetChargeType'] = info.get('InternetChargeType')
            result['SpotStrategy'] = info.get('SpotStrategy')
            result['StoppedMode'] = info.get('StoppedMode')
            result['SerialNumber'] = info.get('SerialNumber')
            result['IoOptimized'] = info.get('IoOptimized')
            result['Memory'] =info.get('Memory')
            result['Cpu'] = info.get('Cpu')
            result['VpcAttributes'] = info.get('VpcAttributes')
            result['InternetMaxBandwidthOut'] = info.get('InternetMaxBandwidthOut')
            result['DeviceAvailable'] = info.get('DeviceAvailable')
            result['SecurityGroupIds'] = info.get('SecurityGroupIds')
            result['SaleCycle'] = info.get('SaleCycle')
            result['SpotPriceLimit'] = info.get('SpotPriceLimit')
            result['AutoReleaseTime'] = info.get('AutoReleaseTime')
            result['StartTime'] = info.get('StartTime')
            result['InstanceName'] = info.get('InstanceName')
            result['Description'] = info.get('Description')
            result['ResourceGroupId'] = info.get('ResourceGroupId')
            result['OSType'] = info.get('OSType')
            result['OSName'] = info.get('OSName')
            result['InstanceNetworkType'] = info.get('InstanceNetworkType')
            result['PublicIpAddress'] = info.get('PublicIpAddress')
            result['HostName'] = info.get('HostName')
            result['InstanceType'] = info.get('InstanceType')
            result['CreationTime']= info.get('CreationTime')
            result['Status'] = info.get('Status')
            result['ClusterId'] = info.get('ClusterId')
            result['Recyclable'] = info.get('Recyclable')
            result['RegionId'] = info.get('RegionId')
            result['GPUSpec'] = info.get('GPUSpec')
            result['OperationLocks'] = info.get('OperationLocks')
            result['InstanceChargeType'] = info.get('InstanceChargeType')
            result['GPUAmount'] = info.get('GPUAmount')
            result['xpiredTime'] = info.get('xpiredTime')
            data.append(result)
        return data


# if __name__ == '__main__':
#     # accessKey='LTAILcALtfLdPgoY'
#     # accessSecret='eAQUuNEBEFT0Eoa1N4FFMZ9R6v3PXY'
#     # region='cn-qingdao'
#
#     print(yunSpider().ECS())