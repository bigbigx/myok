# -*- coding=utf-8 -*-
import logging
import json
from libs import send_email
from libs import baseview
from libs import call_inception
from libs import util
from libs import conn_sqlite
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    DatabaseList,
    SqlOrder,
    Account,
    globalpermissions
)

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')
conf = util.conf_path()
addr_ip = conf.ipaddress


class sqlorder(baseview.BaseView):
    '''
    put   美化sql  测试sql
    post 提交工单
    '''
    def put(self, request, args=None):
        if args == 'beautify':
            #try:
            #    data_select = request.data['data1']
            #    data_ddl_dml = request.data['data2']
            #except KeyError as e:
            #    print("==============")
            #    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            #else:
            try:
                    data_select = request.data['data1']
                    data_ddl_dml = request.data['data2']
                    res={'select':'','dml_ddl':''}
                    data1=''
                    data2=''
                    if data_select !='':
                        data1 = call_inception.Inception.BeautifySQL(sql=data_select)
                    if data_ddl_dml !='':
                        data2 = call_inception.Inception.BeautifySQL(sql=data_ddl_dml)
                    res['select']=data1
                    res['dml_ddl']=data2
                    res=json.dumps(res)
                    return HttpResponse(res)

            except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)

        elif args == 'test':
            try:
                type = int(request.data['type'])
                id = request.data['id']
                base = request.data['base']
                tmp_sql = request.data['sql']
                check_sql = request.data['check_sql']
                sql_ddl = tmp_sql.split('&&&')[0]
                sql_bak= tmp_sql.split('&&&')[1]
                sql_ddl = str(sql_ddl).strip().rstrip(';')
                sql_bak = str(sql_bak).strip().rstrip(';')
                sql_ddl_1 = check_sql.split('&&&')[0]
                sql_bak_1 = check_sql.split('&&&')[1]
                #sql = str(sql).strip('\n').strip().rstrip(';')
                if type == 1:
                    data = DatabaseList.objects.filter(id=id).first()
                else:
                    base_id = request.data['base_id']
                    data = DatabaseList.objects.filter(id=base_id).first()
                info = {
                    'host': data.ip,
                    'user': data.username,
                    'password': data.password,
                    'db': base,
                    'port': data.port
                    }
                if sql_bak_1:
                    myok=sql_bak_1.rstrip().rstrip("\n").rstrip("\r").rstrip("\t").rstrip(";").split(";")
                    for select_sql in myok:

                        tmp=str(select_sql.strip())
                        print("备份语句: " + tmp)
                        if tmp =="":
                            pass
                        else:
                            if (tmp.startswith('SELECT') or tmp.startswith('select')):
                                print("right select")
                                pass
                            else:
                                check_info = "备份SQL语句编辑栏存在非select语句，请注意只能是select 或者SELECT的关键字"
                                return Response({'result': check_info, 'status': 202})

                if sql_ddl_1:
                    for ddl_sql in sql_ddl_1.rstrip().rstrip("\n").rstrip("\r").rstrip(";").split(";"):
                        tmp1=str(ddl_sql.strip())
                        print("执行语句: " + tmp1)
                        if tmp1=="":
                            pass

                        else:
                            if (tmp1.startswith('SELECT') or tmp1.startswith('select')):
                                check_info = "执行SQL编辑栏存在select语句，请检查"
                                return Response({'result': check_info,'status': 202})
                            else:
                                print("right  ddl")
                                pass


            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            else:
                try:
                    with call_inception.Inception(LoginDic=info) as test:
                        res_bak = []
                        res_ddl = []
                        if sql_ddl:
                            res_ddl = test.Check(sql=sql_ddl)
                        if sql_bak:
                           res_bak = test.Check(sql=sql_bak)
                        return Response({'result_ddl': res_ddl,'result_bak': res_bak, 'status': 200})
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return Response({'status': '500'})

    def post(self, request, args=None):
        try:
            data = json.loads(request.data['data'])
            tmp_sql = json.loads(request.data['sql'])
            tmp_bak = json.loads(request.data['backup_sql'])
            user = request.data['user']
            assigned_man=data['assigned']
            type = request.data['type']
            id = request.data['id']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                sql_1=''
                sql_2=''
                if tmp_sql:
                    x = [x.rstrip(';') for x in tmp_sql]
                    sql_1 = ';'.join(x)
                    sql_1 = sql_1.strip(' ').rstrip(';')
                if tmp_bak:
                    k = [k.rstrip(';') for k in tmp_bak]
                    sql_2 = ';'.join(k)
                    sql_2 = sql_2.strip(' ').rstrip(';')

                token = util.generateTokens(32)
                workId = util.workId()
                SqlOrder.objects.get_or_create(
                    username=user,
                    date=util.date(),
                    work_id=workId,
                    status=2,
                    basename=data['basename'],
                    sql=sql_1,
                    type=type,
                    text=data['text'],
                    backup=data['backup'],
                    bundle_id=id,
                    assigned=data['assigned'],
                    backup_sql=sql_2,
                    base_id=id

                    )
#
                content = DatabaseList.objects.filter(id=id).first()
                mail = Account.objects.filter(username=data['assigned']).first()
                tag = globalpermissions.objects.filter(authorization='global').first()
                ret_info = '已提交，请等待管理员审核!'
                if tag is None or tag.dingding == 0:  #  发送町町
                    pass
                else:
                    if content.url:
                        try:
                            util.dingding(
                                content='工单提交通知\n工单编号:%s\n发起人:%s\n地址:%s\n工单说明:%s\n状态:已提交\n备注:%s'
                                        %(workId,user,addr_ip,data['text'],content.before), url=content.url)
                        except:
                            #ret_info = '工单执行成功!但是钉钉推送失败,请查看错误日志排查错误.'
                            ret_info = '工单提交成功!但是钉钉推送失败,请查看错误日志排查错误.'
                # 保存token
                try:
                    #value = [(assigned_man, workId, token)]
                    conn_sqlite.add_one(assigned_man, workId, token)
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)


                if tag is None or tag.email == 0:
                    pass
                else:
                    if mail.email:
                        mess_info = {
                            'workid': workId,
                            #'to_user': user,
                            'to_user': user,
                            'addr': addr_ip,
                            'text': data['text'],
                            'type': "成功发起",
                            'run_sql':sql_1,
                            'backup_sql':sql_2,
                            'status': 'apply',
                            'assigned': assigned_man,
                            'token_pass': token,    # 定义审核通过URL 的token
                            'token_reject': token,  #定义审核驳回URL 的token
                            'note':content.before}
                        try:
                            put_mess = send_email.send_email(to_addr=mail.email)
                            put_mess.send_mail(mail_data=mess_info, type=2)
                        except Exception as e :
                            #ret_info = '工单执行成功!但是邮箱推送失败,请查看错误日志排查错误.'
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            ret_info = '工单提交成功!但是邮箱推送失败,请查看错误日志排查错误.'
                            return HttpResponse(ret_info)


                return Response(ret_info)
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            




#def main():
#    sql='''
#        update t_erp_other_inout t set t.inout_status='complete',t.complete_time='2018-01-16 13:33:39' where t.order_code='H000000375';
#         '''
#    sql_order=sqlorder()
#    sql_order.post(sql)


#if __name__ == '__main__':
#    main()
