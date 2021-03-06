# -*- coding=utf-8 -*-

import logging
import json
from libs import send_email
from libs import baseview
from libs import util
from libs import call_inception
from libs import rollback
from libs import conn_sqlite
from rest_framework.response import Response
from django.db.models import Count
from django.http import HttpResponse
from core.models import (
    SqlOrder,
    Usermessage,
    DatabaseList,
    SqlRecord,
    Account,
    globalpermissions
)
from libs.serializers import (
    Record
)

conf = util.conf_path()
addr_ip = conf.ipaddress
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')


#class audit(baseview.SuperUserpermissions):
class audit(baseview.Approverpermissions):
    '''
    SQL审核相关
    '''
    def get(self, request, args=None):
        try:
            page = request.GET.get('page')
            username = request.GET.get('username')
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                pagenumber = SqlOrder.objects.filter(assigned=username).aggregate(alter_number=Count('id'))
                start = (int(page) - 1) * 20
                end = int(page) * 20
                info = SqlOrder.objects.raw(
                    '''
                    select core_sqlorder.*,core_databaselist.connection_name, \
                    core_databaselist.computer_room from core_sqlorder \
                    INNER JOIN core_databaselist on \
                    core_sqlorder.bundle_id = core_databaselist.id where core_sqlorder.assigned = '%s'\
                    ORDER BY core_sqlorder.id desc
                    '''%username
                )[start:end]
                data = util.ser(info)
                return Response({'page': pagenumber, 'data': data})
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    def put(self, request, args=None):
        try:
            type = request.data['type']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            if type == 0:  #审核驳回
                try:
                    from_user = str(request.data['from_user'])
                    to_user11 = str(request.data['to_user'])
                    text = request.data['text']
                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        data = SqlOrder.objects.filter(id=id).first()
                        try:
                            conn = conn_sqlite.query(from_user, data.work_id)
                        except Exception as e:
                            print(e)
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            ret_info = "sqlite数据库后台异常，请联系系统管理员"
                            return Response(status=500)
                        if conn:  # 如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                            # 执行审核驳回的业务
                                SqlOrder.objects.filter(id=id).update(status=0)
                                _tmpData = SqlOrder.objects.filter(id=id).values(
                                    'work_id',
                                    'bundle_id',
                                    'text',
                                ).first()
                                title = '工单:' + _tmpData['work_id'] + '审核驳回通知'
                                msg_content='工单详情是：' + _tmpData['text'] + '\r\n 驳回意见是： ' + text
                                Usermessage.objects.get_or_create(
                                    from_user=from_user,
                                    time=util.date(),
                                    title=title,
                                    content=msg_content,
                                    to_user=to_user11,
                                    state='unread'
                                )

                                content = DatabaseList.objects.filter(id=_tmpData['bundle_id']).first()
                                mail = Account.objects.filter(username=to_user11).first()
                                tag = globalpermissions.objects.filter(authorization='global').first()
                                ret_info = '操作成功，该请求已驳回！'
                                SqlOrder.objects.filter(id=id).update(reject=text)

                                try:
                                    conn_sqlite.delete(to_user11, data.work_id)
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info = "sqlite数据库后台异常，请联系系统管理员"
                                    return HttpResponse(ret_info)


                                if tag is None or tag.dingding == 0:
                                    pass
                                else:
                                    try:
                                        if content.url:
                                            util.dingding(
                                                content='工单审核驳回通知\n工单编号:%s\n发起人:%s\n地址:%s\n驳回说明:%s\n状态:驳回'
                                                %(_tmpData['work_id'],to_user11,addr_ip,text), url=content.url)
                                    except:
                                        ret_info = '工单审核驳回成功!但是钉钉推送失败,请查看错误日志排查错误.'
                                if tag is None or tag.email == 0:
                                    pass
                                else:
                                    try:
                                        if mail.email:
                                            mess_info = {
                                                'workid':_tmpData['work_id'],
                                                'to_user': to_user11,
                                                'addr': addr_ip,
                                                'type': "审核驳回",
                                                'status':'back',
                                                'text': _tmpData['text'],
                                                'run_sql':data.sql,
                                                'backup_sql':data.backup_sql,
                                                'rejected': text}
                                            put_mess = send_email.send_email(to_addr=mail.email)
                                            put_mess.send_mail(mail_data=mess_info,type=1)
                                    except:
                                        ret_info = '工单审核驳回成功!但是邮箱推送失败,请查看错误日志排查错误.'
                                # ----删除token
                                try:
                                    conn_sqlite.delete(from_user, data.work_id)
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info="sqlite数据库后台异常，请联系系统管理员"
                                    return HttpResponse(ret_info)
                                return Response(ret_info)
                        else:
                            ret_info = '<h1>您已成功进行审核驳回，无需进行二次操作</h1>'
                            return HttpResponse(ret_info)
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)

            elif type == 1:  #审核通过
                try:
                    from_user = request.data['from_user']
                    to_apply = request.data['to_user']
                    to_executer = 'dba'

                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        newtoken = util.generateTokens(32)
                        c = SqlOrder.objects.filter(id=id).first()
                        workid = c.work_id
                        try:
                            conn = conn_sqlite.query(from_user, workid)
                        except Exception as e:
                            print(e)
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            ret_info = "sqlite数据库后台异常，请联系系统管理员"
                            return Response(status=500)
                        if conn :
                           # SqlOrder.objects.filter(id=id).update(status=3)

                            d = Account.objects.filter(group='executer').first()
                            title = f'工单:{c.work_id}审核通过通知'
                            #修改审核状态

                            #############################################
                            SqlOrder.objects.filter(id=id).update(status=1)
                            '''
                            通知消息
    
                            '''
                            Usermessage.objects.get_or_create(
                                from_user=from_user, time=util.date(),
                                title=title, content=f'该工单已审核通过!       \r\n 工单说明是: {c.text}', to_user=to_apply,
                                state='unread'
                            )
                            Usermessage.objects.get_or_create(
                                from_user=from_user, time=util.date(),
                                title=title, content=f'有最新的工单已审核，请执行人执行!       \r\n 工单说明是: {d.username}', to_user=to_apply,
                                state='unread'
                            )

                            '''
    
                            Dingding
    
                            '''
                            data=SqlOrder.objects.filter(id=id).first()
                            content = DatabaseList.objects.filter(id=c.bundle_id).first()
                            mail = Account.objects.filter(username=to_executer).first()
                            mail_exe = Account.objects.filter(username=to_apply).first()
                            tag = globalpermissions.objects.filter(authorization='global').first()
                            #ret_info = '操作成功，该请求已同意!并且已在相应库执行！详细执行信息请前往执行记录页面查看！'
                            ret_info = '该工单已审核通过!'

                               # ----删除审核的token
                            try:
                                conn_sqlite.delete(from_user, data.work_id)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info = "sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                                # -----增加执行的todken
                            try:

                                conn_sqlite.add_one('dba', data.work_id, newtoken)

                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info = "sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                            if tag is None or tag.email == 0:
                                pass
                            else:

                                try:
                                    if mail.email:
                                        mess_info = {
                                            'workid': workid,
                                            'to_user': 'dba',
                                            #'to_executor': d.username,
                                            'addr': addr_ip,
                                            'text': c.text,
                                            'type': "审核成功",
                                            'status':'approve',
                                            'run_sql':data.sql,
                                            'backup_sql':data.backup_sql,
                                            'token_pass':newtoken,
                                            'myself':from_user,
                                            'note': content.after}
                                        put_mess = send_email.send_email(to_addr=mail.email)
                                        put_mess.send_mail(mail_data=mess_info,type=0)
                                        #put_mess1 = send_email.send_email(to_addr=mail_exe.email)
                                        #put_mess1.send_mail(mail_data=mess_info, type=0)
                                except:
                                    #ret_info = '工单执行成功!但是邮箱推送失败,请查看错误日志排查错误.'
                                    ret_info = '工单审核通过!但是邮箱推送失败,请查看错误日志排查错误.'
                                    return HttpResponse(ret_info)

                            return Response(ret_info)
                        else:
                            ret_info = '<h1>您已成功进行审核通过，无需进行二次操作</h1>'
                            return HttpResponse(ret_info)
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)

            elif type == 'test':
                try:
                    base = request.data['base']
                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    sql = SqlOrder.objects.filter(id=id).first()
                    data = DatabaseList.objects.filter(id=sql.bundle_id).first()
                    info = {
                        'host': data.ip,
                        'user': data.username,
                        'password': data.password,
                        'db': base,
                        'port': data.port
                    }
                    try:
                        with call_inception.Inception(LoginDic=info) as test:
                            res = test.Check(sql=sql.sql)
                            return Response({'result': res, 'status': 200})
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return Response({'status': '500'})

    def post(self, request, args: str = None):
        try:
            dataid = json.loads(request.data['id'])
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                for i in dataid:
                    if i['status'] == 1:
                        workid = SqlOrder.objects.filter(id=i['id']).first()
                        SqlRecord.objects.filter(workid=workid.work_id).delete()
                        SqlOrder.objects.filter(id=i['id']).delete()
                    else:
                        SqlOrder.objects.filter(id=i['id']).delete()
                return Response('工单数据删除成功!')
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)


class orderdetail(baseview.BaseView):

    '''

    审核工单的详细信息

    '''
    # 删除工单
    def delelte(self, request, args=None):
        try:
            dataid = request.data['id']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                SqlOrder.objects.filter(id=dataid).delete()
                return Response('工单数据删除成功!')
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    #def get(self, request, args: str = None):
    def get(self, request, args=None):
        try:
            workid = request.GET.get('workid')
            status = request.GET.get('status')
            id = request.GET.get('id')

        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            type_id = SqlOrder.objects.filter(id=id).first()

            try:
                if status == '1':
                    data = SqlRecord.objects.filter(workid=workid).all()
                    _serializers = Record(data, many=True)
                    return Response({'data':_serializers.data, 'type':type_id.type})
                else:
                    data = SqlOrder.objects.filter(work_id=workid).first()
                    print("=====")
                    print(data.backup_sql)
                    mylist=[{'sql': x} for x in data.sql.split(';')]
                    my_bak_list=[{'backup_sql': y} for y in data.backup_sql.split(';')]
                    print(mylist+my_bak_list)

                    _in = {'data': mylist+my_bak_list, 'type': type_id.type}
                    print("+++++")
                    print(_in)
                    return Response(_in)
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__} : {e}')
                return HttpResponse(status=500)

    #def put(self, request, args: str = None):  #  点击进入修改工单SQL
    def put(self, request, args=None):
        try:
            id = request.data['id']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            try:
                info = SqlOrder.objects.raw(
                    "select core_sqlorder.*,core_databaselist.connection_name,\
                    core_databaselist.computer_room from core_sqlorder INNER JOIN \
                    core_databaselist on core_sqlorder.bundle_id = core_databaselist.id \
                    WHERE core_sqlorder.id = %s"
                    %id)
                data = util.ser(info)
                sql = data[0]['sql'].split(';')
                backup_sql = data[0]['backup_sql'].split(';')
                _tmp = ''
                _tmp_1 = ''
                for i in sql:
                    _tmp += i + ";\n"
                for j in backup_sql:
                    _tmp_1 += j + ";\n"
                return Response({'data':data[0], 'sql':_tmp.strip('\n'), 'backup_sql':_tmp_1.strip('\n'),'type': 0})
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    # （查看回滚语句  里面调用到）
    #def post(self, request, args: str = None):
    def post(self, request, args=None):
        try:
            id = request.data['id']
            info = json.loads(request.data['opid'])
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                sql = []
                for i in info:
                    info = SqlOrder.objects.raw(
                        "select core_sqlorder.*,core_databaselist.connection_name,\
                        core_databaselist.computer_room from core_sqlorder INNER JOIN \
                        core_databaselist on core_sqlorder.bundle_id = core_databaselist.id \
                        WHERE core_sqlorder.id = %s"
                        % id)
                    data = util.ser(info)
                    _data = SqlRecord.objects.filter(sequence=i).first()
                    roll = rollback.rollbackSQL(db=_data.backup_dbname, opid=i)
                    link = _data.backup_dbname + '.' + roll
                    spa = rollback.roll(backdb=link, opid=i)
                    sql.append(spa)
                _h=[]
                for i in sql[0]:
                    _h.append(i[0])
                _h = sorted(_h)
                return Response({'data': data[0], 'sql': _h, 'type': 1})
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)



