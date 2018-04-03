'''
 Create your models here.

'''
from django.db import models
from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    '''
    User table
    '''
    #group = models.CharField(max_length=40)   #权限组 guest/admin
    group = models.CharField(max_length=40)   #权限组 guest/approver/executer/admin
    department = models.CharField(max_length=40) #部门


class SqlDictionary(models.Model):
    '''
    数据库字典表
    '''
    BaseName = models.CharField(max_length=100)  #库名
    TableName = models.CharField(max_length=100) #表名
    Field = models.CharField(max_length=100) #字段名
    Type = models.CharField(max_length=100) #类型
    Null = models.CharField(max_length=100) #是否为空
    Default = models.CharField(max_length=100) #默认值
    Extra = models.CharField(max_length=100) #备注
    TableComment = models.CharField(max_length=100) #表备注
    Name = models.CharField(max_length=100, null=True) #连接名

    def __str__(self):
        return self.TableName

class FileContent(models.Model):
    '''
    文件内容表
    '''
    filename =  models.CharField(max_length=50, blank=True)  # 文件名字‘
    filepath =  models.CharField(max_length=50, blank=True)  # 文件路径
    inner_server_ip =  models.CharField(max_length=50, blank=True)  # 文件所在服务器的内部IP
    outer_server_ip = models.CharField(max_length=50, blank=True)  # 文件所在服务器的外部IP
    server_hostname = models.CharField(max_length=50, blank=True)  # 文件所在服务器的主机名
    pg_id =  models.CharField(max_length=50, blank=True)  # 关联的项目的编号
    keyword =  models.CharField(max_length=50, blank=True)  # 搜索的关键字
    file_remark =  models.CharField(max_length=50, blank=True)   # 文件说明YunRdsObj

class YunRdsObj(models.Model):
    LockMode = models.CharField(max_length=300, blank=True)
    DBInstanceNetType = models.CharField(max_length=300, blank=True)
    DBInstanceClass = models.CharField(max_length=300, blank=True)
    ResourceGroupId = models.CharField(max_length=300, blank=True)
    DBInstanceId = models.CharField(max_length=300, blank=True)
    VpcCloudInstanceId = models.CharField(max_length=300, blank=True)
    ZoneId = models.CharField(max_length=300, blank=True)
    ReadOnlyDBInstanceIds = models.CharField(max_length=300, blank=True)
    InstanceNetworkType = models.CharField(max_length=300, blank=True)
    DBInstanceDescription = models.CharField(max_length=300, blank=True)
    ConnectionMode = models.CharField(max_length=300, blank=True)
    Engine = models.CharField(max_length=300, blank=True)
    MutriORsignle = models.CharField(max_length=300, blank=True)
    InsId = models.CharField(max_length=300, blank=True)
    ExpireTime = models.CharField(max_length=300, blank=True)
    CreateTime = models.CharField(max_length=300, blank=True)
    DBInstanceType = models.CharField(max_length=300, blank=True)
    RegionId = models.CharField(max_length=300, blank=True)
    EngineVersion = models.CharField(max_length=300, blank=True)
    LockReason = models.CharField(max_length=300, blank=True)
    DBInstanceStatus = models.CharField(max_length=300, blank=True)
    PayType = models.CharField(max_length=300, blank=True)


class YunEcsObj(models.Model):
    InnerIpAddress = models.CharField(max_length=300, blank=True)
    ImageId= models.CharField(max_length=300, blank=True)
    InstanceTypeFamily= models.CharField(max_length=300, blank=True)
    VlanId= models.CharField(max_length=300, blank=True)
    InstanceId= models.CharField(max_length=300, blank=True)
    EipAddress= models.CharField(max_length=300, blank=True)
    InternetMaxBandwidthIn= models.CharField(max_length=300, blank=True)
    ZoneId= models.CharField(max_length=300, blank=True)
    InternetChargeType= models.CharField(max_length=300, blank=True)
    SpotStrategy= models.CharField(max_length=300, blank=True)
    StoppedMode= models.CharField(max_length=300, blank=True)
    SerialNumber= models.CharField(max_length=300, blank=True)
    IoOptimized= models.CharField(max_length=300, blank=True)
    Memory= models.CharField(max_length=300, blank=True)
    Cpu= models.CharField(max_length=300, blank=True)
    VpcAttributes= models.CharField(max_length=300, blank=True)
    InternetMaxBandwidthOut= models.CharField(max_length=300, blank=True)
    DeviceAvailable= models.CharField(max_length=300, blank=True)
    SecurityGroupIds= models.CharField(max_length=300, blank=True)
    SaleCycle= models.CharField(max_length=300, blank=True)
    SpotPriceLimit= models.CharField(max_length=300, blank=True)
    AutoReleaseTime= models.CharField(max_length=300, blank=True)
    StartTime= models.CharField(max_length=300, blank=True)
    InstanceName= models.CharField(max_length=300, blank=True)
    Description= models.CharField(max_length=300, blank=True)
    ResourceGroupId= models.CharField(max_length=300, blank=True)
    OSType= models.CharField(max_length=300, blank=True)
    OSName= models.CharField(max_length=300, blank=True)
    InstanceNetworkType = models.CharField(max_length=300, blank=True)
    PublicIpAddress = models.CharField(max_length=300, blank=True)
    HostName = models.CharField(max_length=300, blank=True)
    InstanceType = models.CharField(max_length=300, blank=True)
    CreationTime = models.CharField(max_length=300, blank=True)
    Status = models.CharField(max_length=300, blank=True)
    ClusterId = models.CharField(max_length=300, blank=True)
    Recyclable = models.CharField(max_length=300, blank=True)
    RegionId = models.CharField(max_length=300, blank=True)
    GPUSpec = models.CharField(max_length=300, blank=True)
    OperationLocks = models.CharField(max_length=300, blank=True)
    InstanceChargeType = models.CharField(max_length=300, blank=True)
    GPUAmount = models.CharField(max_length=300, blank=True)
    xpiredTime = models.CharField(max_length=300, blank=True)


class YunAssetArea(models.Model):
    '''
    云环境的区域： 如阿里云
    yun_obj:  0--阿里云  1--美团云  2--腾讯云  3 --华为云 等
    area_name: 区域名称： 如华北，华南等
    status  区域的使用状态 :  1--可用 0 --不可用
    '''
    yun_obj = models.IntegerField(blank=True)
    area_name = models.CharField(max_length=50, blank=True)
    status = models.IntegerField(blank=True)

class YunAssetObj(models.Model):
    '''
    云环境的实例类型，如ecs,rds,mq,slb,cdn,等
    '''
    yun_obj = models.IntegerField(blank=True)
    objname = models.CharField(max_length=50, blank=True)
    status = models.IntegerField(blank=True)




class SqlOrder(models.Model):
    '''
    工单提交表
    '''
    work_id = models.CharField(max_length=50, blank=True) #工单id
    username = models.CharField(max_length=50, blank=True) #账号
    #status = models.IntegerField(blank=True) # 工单状态 0 disagree 1 agree 2 indeterminate 3 ongoing
    status = models.IntegerField(blank=True) # 工单状态 0 disagree 1 agree 2 indeterminate 3 ongoing  4 execute reject
    type = models.SmallIntegerField(blank=True) #工单类型 0 DDL 1 DML
    backup = models.SmallIntegerField(blank=True)  # 工单是否备份 0 not backup 1 backup
    bundle_id = models.IntegerField(db_index=True, null=True) # Matching with Database_list id Field
    date = models.CharField(max_length=100, blank=True) # 提交日期
    basename = models.CharField(max_length=50, blank=True) #数据库名
    base_id = models.IntegerField(blank=True)  # 数据库的编号
    sql = models.TextField(blank=True) #sql语句
    text = models.CharField(max_length=300) # 工单备注
    assigned = models.CharField(max_length=50, blank=True)# 工单审核人
    backup_sql=models.TextField(blank=True) #s备份ql语句
    reject = models.TextField(blank=True) #驳回说明
    cc_list = models.CharField(max_length=500, blank=True)# 邮件抄送人
    run_type = models.IntegerField(default=0)# 运行类型



class DatabaseList(models.Model):
    '''
    数据库连接信息表
    '''
    connection_name = models.CharField(max_length=50) #连接名
    computer_room = models.CharField(max_length=50) #机房
    ip = models.CharField(max_length=100) #ip地址
    username = models.CharField(max_length=150) #数据库用户名
    port = models.IntegerField() #端口
    password = models.CharField(max_length=50) #数据库密码
    before = models.TextField(null=True) #提交工单 钉钉webhook发送内容
    after = models.TextField(null=True)  #工单执行成功后 钉钉webhook发送内容
    url = models.TextField(blank=False)    #钉钉webhook url地址

class AssetType(models.Model):
    """
    资产的各种型号
    """

    parent_type = models.IntegerField(null=True, blank=True)
    child_type_1 = models.IntegerField(null=True, blank=True)
    child_type_2 = models.IntegerField(null=True, blank=True)
    child_type_3 = models.IntegerField(null=True, blank=True)
    cab_type = models.CharField(max_length=20, default="暂无", null=True, blank=True)

class AssetTypeDetail(models.Model):
    '''
    资产型号明细表
    '''
    cab_type = models.CharField(max_length=20, default="暂无", null=True, blank=True)  # own,aliyun,other,aws等四个机房
    type_id = models.IntegerField(max_length=20, null=True, blank=True)
    type_name = models.CharField(max_length=20, default="暂无", null=True, blank=True)



class ServerConf(models.Model):
    '''
    服务器配置信息表
    '''
    sudo_choices = (("Y", "使用sudo登陆"), ("N", "普通登陆"))
    su_choices = (("Y", "su - root 登陆"), ("N", "普通登陆"))
    login_type = (("KEY", "使用PublickKey登陆"), ("PASSWORD", "使用密码登陆"))
    IP = models.CharField(max_length=200)
    HostName = models.CharField(max_length=100, null=False, blank=False)
    Port = models.IntegerField()
    Group = models.CharField(max_length=200, null=False, verbose_name="主机组")
    Username = models.CharField(max_length=200, null=False)
    Password = models.CharField(('password'), max_length=128)
    KeyFile = models.CharField(max_length=100, default="N")
    Sudo = models.CharField(max_length=1, choices=sudo_choices, default="N")
    SudoPassword = models.CharField(max_length=2000, null=True, blank=True)
    Su = models.CharField(max_length=1, choices=su_choices, null=True, blank=True, default="N")
    SuPassword = models.CharField(max_length=2000, null=True, blank=True, default="N")
    LoginMethod = models.CharField(max_length=10, choices=login_type, null=True, blank=True, default="N")

class AssetClass(models.Model):
    '''
    设备分类，网络设备，服务器设备，防火墙设备，其他检测入侵设备等
    '''
    class_id = models.IntegerField() # 分类编号
    class_name = models.CharField(max_length=50) # 分类名称
    subclass = models.CharField(max_length=50) # 子分类名称
    introduction = models.TextField(null=True, blank=True)  # 子分类说明

class AssetRoom(models.Model):
    '''
    美团云，阿里云，独立机房和区域信息，1--AWS 2- Aliyun  3--Own 4--Other
    '''
    room_type = models.IntegerField()
    room_id = models.CharField(max_length=200)
    room_name = models.CharField(max_length=200)
    room_remark = models.CharField(max_length=200)

class AssetArea(models.Model):
    '''
    区域信息： 华南区、华北区、等等
    '''
    asset_room_id = models.CharField(max_length=50) #机房编号  0---代表
    status = models.IntegerField()  #使用状态 0--disable  1--enable
    area_id = models.CharField(max_length=50) #区域编号
    area_name = models.CharField(max_length=40) #区域名称
    area_remark = models.CharField(max_length=300) #区域说明

class AssetLifeCycle(models.Model):
    '''
    设备的生命周期，即设备的历史使用情况
    '''
    time = models.CharField(max_length=50) # 使用时间
    content = models.TextField(null=True, blank=True) # 生命期间的使用情况和变更情况，不含部署应用的情况，值包含硬件设备的，以及网络端口连线情况
    cur_status = models.CharField(max_length=50)  #使用时的状态 ，即每一次的设备的变更，含添加硬件等
    cur_person = models.CharField(max_length=300) # 每次变更的操作人，可以是多人，都好分隔

class AssetNet(models.Model):
    '''
    设备的网路接口：
    '''
    name = models.CharField(max_length=50)  #接口名称,
    remark = models.CharField(max_length=300) #此接口介入说明
    status = models.IntegerField()  # 端口的使用状态 1--在使用  2--规划中  3--
    net_id = models.CharField(max_length=50) #网络设备接口编号，含交换机，路由器，防火墙，入侵检测等

class AssetOtherMark(models.Model):
    '''
    设备的其他标识
    '''
    other_identify_id = models.CharField(max_length=50) # 此设备其他标识的编号
    asset_id = models.CharField(max_length=50) #父设备的编号
    mark_name = models.CharField(max_length=50)
    mark_value = models.CharField(max_length=50) # 此设备的值

class Asset(models.Model):  #特别是针对独立机房、阿里云机房
    '''
    硬件设备主表：
    '''
    asset_id = models.CharField(max_length=50) #此设备的编号，通过随机数据构成，
    asset_room = models.CharField(max_length=50) # 此设备所属环境，独立机房，阿里云，美团云，还是其他环境
    asset_area = models.CharField(max_length=50) # 此设备所属区域，如： 广州、华南、北京、等等自定义的属性环境
    parent_asset_id = models.CharField(max_length=50) # 父设备的编号，即此设备被组装到一个大设备里面，default 为空，默认为单独的设备
    asset_class = models.CharField(max_length=50)  # 设备分类，网络设备，服务器设备，防火墙设备，其他检测入侵设备等
    asset_name = models.CharField(max_length=50)  # 设备名称
    description = models.TextField(null=True, blank=True) # 设备描述
    positon = models.CharField(max_length=50)  # 设备所属位置
    isbn = models.CharField(max_length=50)   #设备ISBN号
    CPU = models.CharField(max_length=20, default="暂无", null=True, blank=True)   #设备CPU 信息
    Mem = models.CharField(max_length=20, default="暂无", null=True, blank=True)  #设备内存
    IO = models.CharField(max_length=20, default="暂无", null=True, blank=True) # 设备IO
    other_identify = models.CharField(max_length=50)#设备的其他标识
    Network_id = models.CharField(max_length=50)  #设备的网络接口
    manufacturer = models.CharField(max_length=50)   #产商
    manufacturer_contact = models.CharField(max_length=50)  # 厂商联系人
    manufacturer_fixline = models.CharField(max_length=50)  # 厂商联系官方电话
    manufacturer_mobile = models.CharField(max_length=50)  # 厂商联系电话
    manufacturer_other_contact = models.CharField(max_length=50)  # 厂商其他联系电话
    status = models.IntegerField() #设备的使用状态 0 - 计划购买 1--已购买  2- 已上架,未开机 3-- 运行中  4--已下架  5--已废弃
    lifecycle_id = models.IntegerField() # 设备生命周期编号
    contract_id = models.CharField(max_length=50) # 设备的合同编号
    invoices = models.CharField(max_length=50) # 设备的发票编号
    program_id = models.CharField(max_length=50)  #设备里面的程序清单


class ServerInfo(models.Model):
    IP = models.OneToOneField(ServerConf,on_delete=models.CASCADE,)
    Position = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True, default="请在这里写一个对服务器的描述")
    CPU = models.CharField(max_length=20, default="暂无", null=True, blank=True)
    CPU_process_must = models.CharField(max_length=10, default="暂无", null=True, blank=True)
    MEM_process_must = models.CharField(max_length=10, default="暂无", null=True, blank=True)
    Use_CPU = models.CharField(max_length=20, default="暂无", null=True, blank=True)
    uSE_MEM = models.CharField(max_length=20, default="暂无", null=True, blank=True)
    MEM = models.CharField(max_length=20, default="暂无", null=True, blank=True)
    IO = models.CharField(max_length=200, default="暂无", null=True, blank=True)
    Platform = models.CharField(max_length=200, default="暂无", blank=True)
    System = models.CharField(max_length=200, default="暂无", blank=True)
    InBankWidth = models.IntegerField(null=True, blank=True)
    OutBankWidth = models.IntegerField(null=True, blank=True)
    CurrentUser = models.IntegerField(null=True, blank=True)

class SqlRecord(models.Model):
    '''
    工单执行记录表
    '''
    date = models.CharField(max_length=50) #执行时间
    state = models.CharField(max_length=100) #执行状态
    sql = models.TextField(blank=True) #
    area = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    base = models.CharField(max_length=50)
    error = models.TextField(max_length=500, null=True)
    workid = models.CharField(max_length=50, null=True)
    person = models.CharField(max_length=50, null=True) #执行人
    reviewer = models.CharField(max_length=50, null=True)
    affectrow = models.CharField(max_length=100, null=True)
    sequence = models.CharField(max_length=50, null=True)
    backup_dbname = models.CharField(max_length=100, null=True)
    rollbackid = models.IntegerField(null=True)

class Todolist(models.Model):
    '''
    todo info 
    '''
    username = models.CharField(max_length=50) #账户
    content = models.CharField(max_length=200) #内容

class Usermessage(models.Model):
    '''
    user  message
    '''
    to_user = models.CharField(max_length=50) #收信人
    from_user = models.CharField(max_length=50) #发件人
    content = models.TextField(max_length=500) #内容
    time = models.CharField(max_length=50) #发送时间
    state = models.CharField(max_length=10) #发送状态
    title = models.CharField(max_length=100) # 站内信标题

class globalpermissions(models.Model):
    '''

    globalpermissions

    '''

    dingding = models.SmallIntegerField(default=0)
    email = models.SmallIntegerField(default=0)
    authorization = models.CharField(max_length=50,null=True)
