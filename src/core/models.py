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
    is_master_approve =  models.IntegerField(default=99) # 是否主要审核人还是备用审核人  1--是  0--否  99 --都不是
    is_master_execute =  models.IntegerField(default=99) # 是否主执行人还是备用执行人  1--是  0--否  99 --都不是
    # module_list = models.CharField(max_length=100, blank=True)  # 模块清单

    # workgroup_id = models.CharField(max_length=50, blank=True)  # 工作分组，跟group属性不一样，group是角色分组

# class AccountGroup(models.Model):
#     GroupName = models.CharField(max_length=80)
#     GroupID = models.CharField(max_length=40)
#     PermissonID= models.CharField(max_length=300)  # 权限编号，可以多个，以逗号分割
#     status = models.IntegerField(blank=True) #  0 -- 禁用  1 --启用

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
    文件内容表(含日志)
    '''

    private_server_ip = models.CharField(max_length=50, blank=True)  # 文件所在服务器的内部IP
    public_server_ip = models.CharField(max_length=50, blank=True)  # 文件所在服务器的外部IP
    server_hostname = models.CharField(max_length=50, blank=True)  # 文件所在服务器的主机名
    region_name = models.CharField(max_length=50, blank=True)  # 华北1
    room_name = models.CharField(max_length=50, blank=True)  # 阿里云
    server_status = models.CharField(max_length=50, blank=True)  # running,stopped  主机运行状态
    pg_id = models.CharField(max_length=50, blank=True)  # 关联的项目的编号
    keyword = models.CharField(max_length=50, blank=True)  # 搜索的关键字
    file_title = models.CharField(max_length=300, blank=True)  # 文件标题
    file_type = models.CharField(max_length=50, blank=True)  # 文件类型
    file_path = models.CharField(max_length=50, blank=True)  # 文件路径
    file_remark = models.CharField(max_length=50, blank=True)   # 文件说明YunRdsObj
    file_owner = models.CharField(max_length=400, blank=True)   # 文件归属，可以是多人，都好分隔
    full_file_status = models.CharField(max_length=50, blank=True,default='false') #  全量查看文件的开关  false--禁止， true-- 开启
    visit_way = models.IntegerField(default=1,blank=True) #  0 -- 私网访问  1 --公网访问
    visit_user = models.CharField(max_length=20, blank=True)   # 设置访问用户


class YunRdsObj(models.Model):  #  阿里云的RDS
    Room_id = models.CharField(max_length=300, default='yun001', blank=True)  # 机房或者云环境编号
    Area_id = models.CharField(max_length=300, default='cn_qingdao', blank=True)  #  区域编号
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


class YunEcsObj(models.Model):  #  阿里云的ECS
    Room_id = models.CharField(max_length=300, default='yun001',blank=True)  # 机房或者云环境编号
    Area_id = models.CharField(max_length=300, default='cn_qingdao',blank=True)  # 区域编号
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
    xpiredTime = models.CharField(max_length=300, null=True,blank=True)
    user_pwd_id = models.CharField(max_length=300, null=True,blank=True)  # ecs服务器用户账号密码清单编号

class HostUserPwd(models.Model):
    '''
    服务器用户密码对象表
    '''
    public_IP = models.CharField(max_length=30, blank=True)  # 外网 IP
    private_IP = models.CharField(max_length=30, blank=True) # 内网 IP
    mac_address = models.CharField(max_length=60, blank=True) # 物理地址
    user_name = models.CharField(max_length=30, blank=True)  # 用户名
    password = models.CharField(max_length=50, blank=True)  # ssh登录密码
    remark = models.CharField(max_length=300, blank=True)  # 用户说明
    type = models.IntegerField(blank=True)  # 账号分类  0--超级管理员  1--高级管理员  2 --普通用户 3 --   99--guest
    status = models.IntegerField(blank=True)  # 启用状态  0--禁用   1-- 启用
    server_status = models.IntegerField(blank=True, default=1)  # 服务器启用状态  0--禁用   1-- 启用
    workgroup_id = models.CharField(max_length=30, blank=True)  # 工作组编号，此账号分配给的工作组

class ConfigAccount(models.Model):
    user_id = models.IntegerField(default=1, blank=True)  # 用户编号
    module_code = models.CharField(max_length=50, blank=True) # 用户拥有的模块编号



class Config(models.Model):
    code = models.CharField(max_length=50, blank=True)  # 配置编号
    name = models.CharField(max_length=50, blank=True)  # 配置名称
    type = models.IntegerField(default=1, blank=True)  # 配置类型编号  1--平台模块 2--系统配置
    flow_or_not = models.IntegerField(default=1, blank=True)  # 配置类型编号  1----需要走流程  0---不需要走流程
    type_name = models.CharField(max_length=50, blank=True)  # 配置类型
    status = models.CharField(max_length=50, blank=True) #配置启用状态
    remark = models.CharField(max_length=50, blank=True) # 配置备注

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
    computer_room = models.CharField(max_length=100, blank=True) # 机房名称
    connection_name = models.CharField(max_length=100, blank=True) # 连接名
    basename = models.CharField(max_length=50, blank=True) #数据库名
    base_id = models.IntegerField(blank=True,null=True)  # 数据库的编号
    sql = models.TextField(blank=True) #sql语句
    text = models.CharField(max_length=300) # 工单备注
    system = models.CharField(max_length=300,blank=True) # 被影响到的应用系统
    approve_man = models.CharField(max_length=50, blank=True)# 工单审核人
    execute_man = models.CharField(max_length=50, blank=True)# 工单执行人
    approvetime = models.CharField(max_length=50, blank=True)# 工单审核时间
    runtime = models.CharField(max_length=50, blank=True)# 工单执行时间
    backup_sql=models.TextField(blank=True,null=True) #s备份ql语句
    reject = models.TextField(blank=True,null=True) #驳回说明
    pass_remark = models.TextField(blank=True,null=True) #审核同意备注
    cc_list = models.CharField(max_length=500, blank=True,null=True)# 邮件抄送人
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
