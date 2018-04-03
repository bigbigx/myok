




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