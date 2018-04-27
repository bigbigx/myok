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

#class SqlOrderBak(models.Model):
#    '''
#    工单sql备份主表#
#
#    '''
#    work_id = models.CharField(max_length=50, blank=True) #工单id
#    sql = models.TextField(blank=True) #sql语句
##    order_id = models.IntegerField(blank=True) #执行顺序
#   status = models.IntegerField(blank=True)是 #此条SQL备份状态


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
    approve_time_new =  models.CharField(max_length=50, blank=True)# 工单审核时间
    backup_sql=models.TextField(blank=True) #s备份ql语句
    reject = models.TextField(blank=True) #驳回说明
    run_type = models.IntegerField(null=True,blank=True) #执行SQL的方式 0 ---inception提交和执行  1--直接连接数据库执行sql
    cc_list = models.CharField(max_length=500, blank=True) #该工单邮件抄送人清单


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
    url = models.TextField(blank=True)    #钉钉webhook url地址


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
