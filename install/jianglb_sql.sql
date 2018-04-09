




1、增加redis缓存机制，对于asset或者host等常用信息，放置在redis下，
   两种情况更新redis:

    (1) redis已经没有数据，第一次先去mysql查询，同时同步到redis,然后后面的查询都去到redis;

    (2) asset数据库的更新，会马上同步到mysql,然后马上同步到redis (大概两分钟)，如果查询到redis 没有更新后的数据，马上去mysql里面查询




2、增加阿里云ecs的model
InnerIpAddress
ImageId
InstanceTypeFamily
VlanId
InstanceId
EipAddress
InternetMaxBandwidthIn
ZoneId
InternetChargeType
SpotStrategy
StoppedMode
SerialNumber
IoOptimized
Memory
Cpu'
VpcAttributes
InternetMaxBandwidthOut
DeviceAvailable
SecurityGroupIds
SaleCycle
SpotPriceLimit
AutoReleaseTime
StartTime)
InstanceName
Description
ResourceGroupId
OSType
OSName
InstanceNetworkType
PublicIpAddress
HostName
InstanceType
CreationTime
Status
ClusterId
Recyclable
RegionId
GPUSpec
OperationLocks
InstanceChargeType
GPUAmount
xpiredTime

3、新增rds的model

LockMode
DBInstanceNetType
DBInstanceClass
ResourceGroupId
DBInstanceId
VpcCloudInstanceId
ZoneId
ReadOnlyDBInstanceIds
InstanceNetworkType
DBInstanceDescription
ConnectionMode
Engine
MutriORsignle
InsId
ExpireTime
CreateTime
DBInstanceType
RegionId
EngineVersion
LockReason
DBInstanceStatus
PayType

3、  AssetArealist 表添加初始数据
insert into core_assetarealist values(2,'yun001','阿里云','cn-beijing','华北2',1,'');
insert into core_assetarealist values(3,'yun001','阿里云','cn-hangzhou','华东1',1,'');
insert into core_assetarealist values(4,'yun001','阿里云','cn-shangha','华东2',1);
insert into core_assetarealist values(5,'yun001','阿里云','cn-shenzhen','华南1',1);
insert into core_assetarealist values(6,'yun001','阿里云','cn-hongkong','香港',1);
insert into core_assetarealist values(7,'yun001','阿里云','ap-southeast-1','亚太东南1',1);
insert into core_assetarealist values(8,'yun001','阿里云','ap-southeast-2','亚太东南2',1);
insert into core_assetarealist values(9,'yun001','阿里云','ap-southeast-3','亚太东南3',1);
insert into core_assetarealist values(10,'yun001','阿里云','ap-northeast','亚太东北1',1);
insert into core_assetarealist values(11,'yun001','阿里云','us-west-1','美国西部1',1);
insert into core_assetarealist values(12,'yun001','阿里云','us-east-1','美国东部1',1);
insert into core_assetarealist values(13,'yun001','阿里云','eu-central-1','欧洲中部1',1);
insert into core_assetarealist values(14,'yun001','阿里云','me-east-1','中东中部1',1);