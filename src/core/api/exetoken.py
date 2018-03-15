# -*- coding=utf-8 -*-
import logging
import json
from libs import send_email
from libs import baseview
from libs import util
from libs import conn_sqlite
from libs import exportexcel
from libs import call_inception
from libs.serializers import SqlRecord
import time
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    SqlOrder,
    Usermessage,
    DatabaseList,
    Account,
    globalpermissions
)
from libs.serializers import (
    Record
)

conf = util.conf_path()
addr_ip = conf.ipaddress
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

class exetoken(baseview.AnyLogin):
    '''
    SQL 执行通过或者执行驳回的方法，通过按钮的URL传参过来
    '''

    def get(self, request, args=None):
            try:
                type = int(request.GET.get('type'))
            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                if type == 0:  # 执行驳回
                    token = request.GET.get('mytoken')
                    workid = request.GET.get('workid')
                    username = request.GET.get('username')
                    text = "手工驳回，详情请联系执行人"
                    to_user = request.GET.get('to_user')
                    ret_info = ""
                    try:
                        mail = Account.objects.filter(username=username).first()
                        mail_exe = Account.objects.filter(username='dba').first()
                        # tag = globalpermissions.objects.filter(authorization='global').first()

                        try:
                            #username='dba'
                            conn = conn_sqlite.query(to_user, workid)
                        except Exception as e:
                            print(e)
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            ret_info = "sqlite数据库后台异常，请联系系统管理员"
                            return Response(status=500)

                        if conn:  # 如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                            #SqlOrder.objects.filter(id=id).update(status=0)
                            SqlOrder.objects.filter(work_id=workid).update(status=3)  # 修改工单状态为执行驳回
                            _tmpData = SqlOrder.objects.filter(work_id=workid).values(
                                'work_id',
                                'bundle_id',
                                'text'
                            ).first()
                            reject_remark = '快捷执行驳回，具体驳回原因请联系审核人: ' + mail_exe.email
                            title = '工单:' + _tmpData['work_id'] + '执行驳回通知'
                            msg_content = '工单详情是：' + _tmpData['text'] + '\n 驳回意见是： ' + text
                            Usermessage.objects.get_or_create(
                                from_user=username,
                                time=util.date(),
                                title=title,
                                content=msg_content,
                                to_user=to_user,
                                state='unread'
                            )
                            data = SqlOrder.objects.filter(work_id=workid).first()
                            content = DatabaseList.objects.filter(id=_tmpData['bundle_id']).first()
                            mail = Account.objects.filter(username=to_user).first()
                            tag = globalpermissions.objects.filter(authorization='global').first()
                            ret_info = '<h1>操作成功，该执行请求已驳回！</h1>'


                            # ----删除执行token 执行驳回
                            try:

                                conn_sqlite.deleteByToken(token)
                                print("删除token成功")
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info="sqlite数据库后台异常，请联系系统管理员"
                                return Response(status=500)



                            if tag is None or tag.email == 0:
                                pass
                            else:
                                try:
                                    if mail.email:
                                        mess_info = {
                                            'workid':_tmpData['work_id'],
                                            'to_user':to_user,
                                            'addr': addr_ip,
                                            'type': "执行驳回",
                                            'text': data.text,
                                            'status':'run_back',
                                            'rejected': reject_remark}
                                        put_mess = send_email.send_email(to_addr=mail.email)
                                        put_mess.send_mail(mail_data=mess_info,type=4)
                                except:
                                    ret_info = '<h1>工单执行驳回成功!但是邮箱推送失败,请查看错误日志排查错误.</h1>'
                            return HttpResponse(ret_info)

                        else:  # 不存在token,直接返回异常
                            ret_info = '<h1>您已成功进行审核，无需进行二次操作</h1>'
                            return HttpResponse(ret_info)
                    except:
                        ret_info = '<h1> 访问服务器异常</h1>'
                        return HttpResponse(ret_info)

                elif type == 1:  #   执行，发送信息和邮件给到工单发起人和审核人
                        token = request.GET.get('mytoken')
                        workid = request.GET.get('workid')
                        username = request.GET.get('username')
                        to_user = request.GET.get('to_user')
                        print("===============++++")
                        ret_info=""
                        try:
                            mail = Account.objects.filter(username=username).first()
                            #tag = globalpermissions.objects.filter(authorization='global').first()


                            try:
                                conn = conn_sqlite.queryByToken(token)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info="sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                            if conn:  #如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                                try:  # 备份sql语句

                                    c = SqlOrder.objects.filter(work_id=workid).first()
                                    SQL_LIST = DatabaseList.objects.filter(id=c.bundle_id).first()
                                    sql_data = SqlOrder.objects.filter(work_id=workid).first()
                                    bak_sql = sql_data.backup_sql
                                    file_path = []
                                    # print(bak_sql)
                                    backup_status = ''
                                    if bak_sql is not None:
                                        backup_status = '备份成功'
                                        for x in bak_sql.split(';'):
                                            # print(x)
                                            if x.strip() == '':
                                                print('pass')
                                                continue
                                            else:
                                                cur_time = time.strftime('%Y-%m-%d_%H-%M-%S',
                                                                         time.localtime(time.time()))
                                                work_id = c.work_id
                                                outputpath = 'xls/' + work_id + '-' + cur_time + '.xls'
                                                exportexcel.exportExcel(SQL_LIST.ip, SQL_LIST.username,
                                                                        SQL_LIST.password, c.basename,
                                                                        SQL_LIST.port, x, outputpath)
                                                file_path.append(outputpath)
                                    else:
                                        print('pass-pass')
                                        pass

                                except Exception as e:
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    return HttpResponse(status=500)  # 备份失败退出

                                try:
                                    SqlOrder.objects.filter(work_id=workid).update(status=5)  # 执行中
                                    # c = SqlOrder.objects.filter(id=id).first()  # 前面已经执行
                                    title = f'工单:{c.work_id}执行成功通知'
                                    '''
                                    根据工单编号拿出对应sql的拆解数据
                                 '''
                                    # SQL_LIST = DatabaseList.objects.filter(id=c.bundle_id).first() #前面已经执行
                                    '''
                                    发送sql语句到inception中执行
                                 '''
                                    res = []
                                    if c.sql:
                                        with call_inception.Inception(
                                                LoginDic={
                                                    'host': SQL_LIST.ip,
                                                    'user': SQL_LIST.username,
                                                    'password': SQL_LIST.password,
                                                    'db': c.basename,
                                                    'port': SQL_LIST.port
                                                }
                                        ) as f:
                                            res = f.Execute(sql=c.sql, backup=c.backup)
                                            SqlOrder.objects.filter(work_id=workid).update(status=4)
                                    else:
                                        pass


                                except Exception as e:
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    SqlOrder.objects.filter(work_id=workid).update(status=1)  # 状态回滚
                                    return HttpResponse(status=500)

                                try:
                                    '''
                                        修改该工单编号的state状态 ---修改为执行成功状态
                                    '''

                                    # 同时修改时间戳
                                    #cur_time = int(time.time())
                                    '''
                                        遍历返回结果插入到执行记录表中
                                    '''
                                    for i in res:
                                        SqlRecord.objects.get_or_create(
                                            date=util.date(),
                                            state=i['stagestatus'],
                                            sql=i['sql'],
                                            area=SQL_LIST.computer_room,
                                            name=SQL_LIST.connection_name,
                                            error=i['errormessage'],
                                            base=c.basename,
                                            workid=c.work_id,
                                            person=username,
                                            # reviewer=c.assigned,
                                            reviewer='dba',
                                            affectrow=i['affected_rows'],
                                            sequence=i['sequence'],
                                            backup_dbname=i['backup_dbname'],
                                            # execute_time=i['execute_time']
                                        )
                                    '''
                                    通知消息
                                    '''
                                    Usermessage.objects.get_or_create(
                                        from_user=username, time=util.date(),
                                        # title=title, content='该工单已执行成功!', to_user=to_user,
                                        title=title, content=f'该工单已执行成功！ 工单说明是: {c.text}', to_user=c.username,
                                        state='unread'
                                    )

                                    Usermessage.objects.get_or_create(
                                        from_user=username, time=util.date(),
                                        # title=title, content='该工单已执行成功!', to_user=to_user,
                                        title=title, content=f'该工单已执行成功！ 工单说明是: {c.text}', to_user=to_user,  # 发送给发起人
                                        state='unread'
                                    )
                                    Usermessage.objects.get_or_create(
                                        from_user=username, time=util.date(),
                                        # title=title, content='该工单已执行成功!', to_user=to_user,
                                        title=title, content=f'该工单已执行成功！ 工单说明是: {c.text}', to_user=username,  # 发给审核人
                                        state='unread'
                                    )

                                    '''
                                    Dingding
                                    '''

                                    content = DatabaseList.objects.filter(id=c.bundle_id).first()
                                    mail = Account.objects.filter(username=to_user).first()
                                    mail_approver = Account.objects.filter(username=username).first()
                                    tag = globalpermissions.objects.filter(authorization='global').first()
                                    ret_info = '操作成功，该执行请求已经完成!并且已在相应库执行！详细执行信息请前往执行记录页面查看！'

                                    if tag is None or tag.dingding == 0:
                                        pass
                                    else:
                                        try:
                                            if content.url:
                                                util.dingding(
                                                    content='工单执行成功通知\n工单编号:%s\n发起人:%s\n地址:%s\n工单备注:%s\n状态:同意\n备注:%s'
                                                            % (c.work_id, c.username, addr_ip, c.text, content.after),
                                                    url=content.url)


                                        except:
                                            ret_info = '工单执行成功!但是钉钉推送失败,请查看错误日志排查错误.'

                                    if tag is None or tag.email == 0:
                                        pass
                                    else:
                                        try:
                                            if mail.email:
                                                mess_info = {
                                                    'workid': c.work_id,
                                                    'to_user': c.username,
                                                    'approver': to_user,
                                                    'run_sql': c.sql,
                                                    'backup_sql': bak_sql,
                                                    'addr': addr_ip,
                                                    'text': c.text,
                                                    'status': 'run',
                                                    'type': '执行成功',
                                                    'backup': backup_status,
                                                    'note': content.after,
                                                    'file': file_path}
                                                put_mess = send_email.send_email(to_addr=mail.email)
                                                put_mess.send_mail(mail_data=mess_info, type=3)
                                                put_mess1 = send_email.send_email(to_addr=mail_approver.email)
                                                put_mess1.send_mail(mail_data=mess_info, type=3)
                                        except Exception as e:
                                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                            ret_info = '工单执行成功!但是邮箱推送失败,请查看错误日志排查错误.'
                                            return HttpResponse(ret_info)
                                except Exception as e:
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    return HttpResponse(status=500)

                                # ----删除token

                                try:

                                    conn_sqlite.delete(to_user, workid)
                                    print("删除成功")
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    #ret_info="sqlite数据库后台异常，请联系系统管理员"
                                    return HttpResponse(status=500)
                                ret_info = '<h1>已执行</h1>'
                                return HttpResponse(ret_info)

                            else:  #不存在token,直接返回异常
                                ret_info='<h1>您已成功执行SQL，无需进行二次操作</h1>'
                                return HttpResponse(ret_info)
                        except:
                            ret_info='<h1> 访问服务器异常</h1>'
                            return HttpResponse(ret_info)

    def put(self, request, args=None):
            pass

    def post(self, request, args: str = None):
            pass
