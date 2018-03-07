import logging
import json
from libs import send_email
from libs import baseview
from libs import call_inception
from libs import util
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
            try:
                data_select = request.data['data1']
                print(data_select)
                data_ddl_dml = request.data['data2']
                print(data_ddl_dml)
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            else:
                try:
                    res={'select':'','dml_ddl':''}
                    data1 = call_inception.Inception.BeautifySQL(sql=data_select)
                    data2 = call_inception.Inception.BeautifySQL(sql=data_ddl_dml)
                    res['select']=data1
                    res['dml_ddl']=data2
                    print(res)
                    res=json.dumps(res)
                    return HttpResponse(res)

                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)

        elif args == 'test':
            try:
                id = request.data['id']
                base = request.data['base']
                sql = request.data['sql']
                sql = str(sql).strip('\n').strip().rstrip(';')
                data = DatabaseList.objects.filter(id=id).first()
                info = {
                    'host': data.ip,
                    'user': data.username,
                    'password': data.password,
                    'db': base,
                    'port': data.port
                    }
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            else:
                try:
                    with call_inception.Inception(LoginDic=info) as hello:
                        res = hello.Check(sql=sql)
                        print(res)
                        return Response({'result': res, 'status': 200})
                except Exception as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return Response({'status': '500'})

    def post(self, request, args=None):
        try:
            data = json.loads(request.data['data'])
            tmp = json.loads(request.data['sql'])

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
                x = [x.rstrip(';') for x in tmp]
                sql = ';'.join(x)
                sql = sql.strip(' ').rstrip(';')

                k = [k.rstrip(';') for k in tmp_bak]
                sql_bak = ';'.join(k)
                sql_bak = sql_bak.strip(' ').rstrip(';')


                workId = util.workId()
                SqlOrder.objects.get_or_create(
                    username=user,
                    date=util.date(),
                    work_id=workId,
                    status=2,
                    basename=data['basename'],
                    sql=sql,
                    type=type,
                    text=data['text'],
                    backup=data['backup'],
                    bundle_id=id,
                    assigned=data['assigned'],
                    backup_sql=sql_bak
                    )
#
                content = DatabaseList.objects.filter(id=id).first()
                mail = Account.objects.filter(username=data['assigned']).first()
                tag = globalpermissions.objects.filter(authorization='global').first()
                ret_info = '已提交，请等待管理员审核!'
                if tag is None or tag.dingding == 0:
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
                            'status':'apply',
                            'note': content.before}
                        try:
                            put_mess = send_email.send_email(to_addr=mail.email)
                            put_mess.send_mail(mail_data=mess_info, type=2)
                        except:
                            #ret_info = '工单执行成功!但是邮箱推送失败,请查看错误日志排查错误.'
                            ret_info = '工单提交成功!但是邮箱推送失败,请查看错误日志排查错误.'
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
