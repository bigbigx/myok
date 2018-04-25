import logging
import json
from libs import send_email
from libs import baseview
from libs import util
from libs import conn_sqlite
from libs import call_inception
from libs import call_explain
from libs import rollback
from libs import exportexcel

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
import time
from libs.serializers import (
    Record
)

conf = util.conf_path()
addr_ip = conf.ipaddress

CUSTOM_ERROR = logging.getLogger('Yearning.core.views')


# class execute(baseview.SuperUserpermissions):
class execute(baseview.Approverpermissions):
    '''
    SQL执行相关
    '''

    ### 执行获取清单,只获取审核同意的，
    def get(self, request, args=None):
        try:
            page = request.GET.get('page')
            username = request.GET.get('username')
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            return HttpResponse(status=500)
        else:
            try:
                # pagenumber = SqlOrder.objects.filter(assigned=username).aggregate(alter_number=Count('id'))
                pagenumber = SqlOrder.objects.filter(status=1).aggregate(alter_number=Count('id'))
                start = (int(page) - 1) * 20
                end = int(page) * 20
                # '''
                # select core_sqlorder.*,core_databaselist.connection_name, \
                # core_databaselist.computer_room from core_sqlorder \
                # INNER JOIN core_databaselist on \
                # core_sqlorder.bundle_id = core_databaselist.id where core_sqlorder.assigned = '%s' and core_sqlorder.status=1 \
                # ORDER BY core_sqlorder.id desc
                # '''%username
                info = SqlOrder.objects.raw(
                    '''
                    select core_sqlorder.*,core_databaselist.connection_name, \
                    core_databaselist.computer_room from core_sqlorder \
                    INNER JOIN core_databaselist on \
                    core_sqlorder.bundle_id = core_databaselist.id where core_sqlorder.status=1 \
                    ORDER BY core_sqlorder.id desc
                    '''
                )[start:end]
                data = util.ser(info)
                return Response({'page': pagenumber, 'data': data})
            except Exception as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)

    ###执行---检测和执行驳回和执行提交
    def put(self, request, args=None):
        try:
            type = request.data['type']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            if type == 0:  # 执行驳回
                try:
                    from_user = request.data['from_user']
                    to_user = request.data['to_user']
                    text = request.data['text']
                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        try:
                            data = SqlOrder.objects.filter(id=id).first
                            conn = conn_sqlite.query(from_user, data.work_id)
                        except Exception as e:
                            print(e)
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            ret_info = "sqlite数据库后台异常，请联系系统管理员"
                            return Response(status=500)
                        if conn:  # 如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                            # SqlOrder.objects.filter(id=id).update(status=0)
                            SqlOrder.objects.filter(id=id).update(status=3)
                            _tmpData = SqlOrder.objects.filter(id=id).values(
                                'work_id',
                                'bundle_id',
                                'text'
                            ).first()
                            title = '工单:' + _tmpData['work_id'] + '执行驳回通知'
                            msg_content = '工单详情是：' + _tmpData['text'] + '\n 驳回意见是： ' + text
                            Usermessage.objects.get_or_create(
                                from_user=from_user,
                                time=util.date(),
                                title=title,
                                content=msg_content,
                                to_user=to_user,
                                state='unread'
                            )

                            content = DatabaseList.objects.filter(id=_tmpData['bundle_id']).first()
                            mail = Account.objects.filter(username=to_user).first()
                            tag = globalpermissions.objects.filter(authorization='global').first()
                            ret_info = '操作成功，该执行请求已驳回！'

                            if tag is None or tag.dingding == 0:
                                pass
                            else:
                                try:
                                    if content.url:
                                        util.dingding(
                                            content='工单执行驳回通知\n工单编号:%s\n发起人:%s\n地址:%s\n驳回说明:%s\n状态:驳回'
                                                    % (_tmpData['work_id'], to_user, addr_ip, text), url=content.url)
                                except:
                                    ret_info = '工单执行驳回成功!但是钉钉推送失败,请查看错误日志排查错误.'

                            # ----删除执行token 执行驳回
                            try:

                                conn_sqlite.delete(to_user, data.work_id)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                # ret_info="sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(status=500)

                            if tag is None or tag.email == 0:
                                pass
                            else:
                                try:
                                    if mail.email:
                                        mess_info = {
                                            'workid': _tmpData['work_id'],
                                            'to_user': to_user,
                                            'addr': addr_ip,
                                            'type': "执行驳回",
                                            'status': 'run_back',
                                            'rejected': text}
                                        put_mess = send_email.send_email(to_addr=mail.email)
                                        put_mess.send_mail(mail_data=mess_info, type=4)
                                except:
                                    ret_info = '工单执行驳回成功!但是邮箱推送失败,请查看错误日志排查错误.'
                            return Response(ret_info)
                        else:
                            ret_info = '<h1>您已成功执行SQL，无需进行二次操作</h1>'
                            return HttpResponse(ret_info)
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)

            elif type == 1:  ##开始执行, 邮件发送到发起人，审核人和抄送人员
                try:
                    from_user = request.data['from_user']
                    to_user = request.data['to_user']
                    # username = request.data['username']
                    # token=request.data['token']
                    # backup_sql=request.data['backup_sql']
                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:

                    try:
                        c = SqlOrder.objects.filter(id=id).first()
                        run_type_value = c.run_type
                        sql_value = c.sql
                        workid = c.work_id
                        cc_list = c.cc_list
                        conn = conn_sqlite.query(from_user, workid)  # 查询token 是否存在
                    except Exception as e:
                        print(e)
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        ret_info = "sqlite数据库后台异常，请联系系统管理员"
                        return HttpResponse(ret_info)
                    if conn:
                        try:  # 备份sql语句

                            SQL_LIST = DatabaseList.objects.filter(id=c.bundle_id).first()
                            sql_data = SqlOrder.objects.filter(id=id).first()
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
                                        cur_time = time.strftime('%Y-%m-%d_%H-%M-%S-%f', time.localtime(time.time()))
                                        work_id = c.work_id
                                        outputpath = 'xls/' + work_id + '-' + cur_time + '.xls'
                                        exportexcel.exportExcel(SQL_LIST.ip, SQL_LIST.username, SQL_LIST.password,
                                                                c.basename,
                                                                SQL_LIST.port, x, outputpath)
                                        file_path.append(outputpath)
                            else:
                                print('pass-pass')
                                pass

                        except Exception as e:
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            return HttpResponse(status=500)  # 备份失败退出

                        try:
                            SqlOrder.objects.filter(id=id).update(status=5)  # 执行中
                            # c = SqlOrder.objects.filter(id=id).first()  # 前面已经执行
                            title = f'工单:{c.work_id}执行成功通知'
                            '''
                            根据工单编号拿出对应sql的拆解数据
                         '''
                            # SQL_LIST = DatabaseList.objects.filter(id=c.bundle_id).first() #前面已经执行
                            '''
                            
                         '''

                            if c.run_type == 0:  # 发送sql语句到inception中执行
                                res = []
                                res_explain = []
                                if sql_value:
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
                                        SqlOrder.objects.filter(id=id).update(status=4)
                                else:
                                    pass
                            else:  # 发送sql语句到后台数据库中直接执行
                                if sql_value:
                                    with  call_explain.Explain(LoginDic={
                                        'host': SQL_LIST.ip,
                                        'user': SQL_LIST.username,
                                        'password': SQL_LIST.password,
                                        'db': c.basename,
                                        'port': SQL_LIST.port
                                    }) as test:
                                        for i_sql in str(sql_value).split(';'):
                                            res_explain = test.RunSQL(sql=i_sql)
                                        SqlOrder.objects.filter(id=id).update(status=4)

                        except Exception as e:
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            print(f'{e.__class__.__name__}: {e}')
                            SqlOrder.objects.filter(id=id).update(status=1)  # 状态回滚
                            return HttpResponse(status=500)
                        try:
                            '''
                                修改该工单编号的state状态 ---修改为执行成功状态
                            '''

                            # 同时修改时间戳
                            # cur_time=int(time.time())
                            '''
                                遍历返回结果插入到执行记录表中
                            '''
                            if c.run_type == 1:
                                SqlRecord.objects.get_or_create(
                                    date=util.date(),
                                    state='done',
                                    sql=sql_value + ';',
                                    area=SQL_LIST.computer_room,
                                    name=SQL_LIST.connection_name,
                                    error='0',
                                    base=c.basename,
                                    workid=c.work_id,
                                    person=c.username,
                                    # reviewer=c.assigned,
                                    reviewer=from_user,
                                    affectrow='',
                                    sequence='',
                                    backup_dbname='',
                                    # execute_time=i['execute_time']
                                )
                            else:
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
                                        person=c.username,
                                        # reviewer=c.assigned,
                                        reviewer=from_user,
                                        affectrow=i['affected_rows'],
                                        sequence=i['sequence'],
                                        backup_dbname=i['backup_dbname'],
                                    )
                            ''' 
                            通知消息
                            '''
                            Usermessage.objects.get_or_create(
                                from_user=from_user, time=util.date(),
                                # title=title, content='该工单已执行成功!', to_user=to_user,
                                title=title, content=f'该工单已执行成功！ 工单说明是: {c.text}', to_user=c.username,
                                state='unread'
                            )

                            Usermessage.objects.get_or_create(
                                from_user=from_user, time=util.date(),
                                # title=title, content='该工单已执行成功!', to_user=to_user,
                                title=title, content=f'该工单已执行成功！ 工单说明是: {c.text}', to_user=to_user,  # 发送给发起人
                                state='unread'
                            )
                            Usermessage.objects.get_or_create(
                                from_user=from_user, time=util.date(),
                                # title=title, content='该工单已执行成功!', to_user=to_user,
                                title=title, content=f'该工单已执行成功！ 工单说明是: {c.text}', to_user=from_user,  # 发给审核人
                                state='unread'
                            )

                            '''
                            Dingding
                            '''

                            content = DatabaseList.objects.filter(id=c.bundle_id).first()
                            mail_apply = Account.objects.filter(username=c.username).first()  # 工单发起人
                            mail_approver = Account.objects.filter(username=to_user).first()  # 指派人，即审核人
                            tag = globalpermissions.objects.filter(authorization='global').first()
                            ret_info = '操作成功，该执行请求已经完成!并且已在相应库执行！详细执行信息请前往执行记录页面查看！'
                            #
                            # if tag is None or tag.dingding == 0:
                            #     pass
                            # else:
                            #     try:
                            #         if content.url:
                            #             util.dingding(
                            #                 content='工单执行成功通知\n工单编号:%s\n发起人:%s\n地址:%s\n工单备注:%s\n状态:同意\n备注:%s'
                            #                         % (c.work_id, c.username, addr_ip, c.text, content.after),
                            #                 url=content.url)
                            #
                            #
                            #     except:
                            #         ret_info = '工单执行成功!但是钉钉推送失败,请查看错误日志排查错误.'

                            if tag is None or tag.email == 0:
                                pass
                            else:
                                try:
                                    if mail_apply.email:
                                        mess_info = {
                                            'workid': c.work_id,
                                            'to_user': c.username,
                                            'approver': to_user,
                                            'approve_man': mail_approver.email,
                                            'run_sql': c.sql,
                                            'backup_sql': bak_sql,
                                            'addr': addr_ip,
                                            'text': c.text,
                                            'status': 'run',
                                            'type': '执行成功',
                                            'backup': backup_status,
                                            'note': content.after,
                                            'approver_mail': mail_approver.email,
                                            'cc_list': cc_list,
                                            'file': file_path}
                                        put_mess = send_email.send_email(to_addr=mail_apply.email)  # 发功给申请人
                                        put_mess.send_mail(mail_data=mess_info, type=3)
                                except Exception as e:
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info = '工单执行成功!但是邮箱推送给工单发起人 %s失败,请查看错误日志排查错误.' %  (c.username)

                            # 删除执行人的token
                            try:
                                conn_sqlite.delete('dba', workid)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info = "sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                            return Response(ret_info)
                        except Exception as e:
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            return HttpResponse(status=500)
                    else:
                        ret_info = '<h1>您已成功执行SQL，无需进行二次操作</h1>'
                        return HttpResponse(ret_info)

            elif type == 'test':  ## 含ddl & dml检测和sql备份语句显示
                try:
                    base = request.data['base']
                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    ddl_sql_list = []
                    backup_sql_list = []
                    res = {'ddl_sql': ddl_sql_list, 'backup_sql': backup_sql_list}
                    sql = SqlOrder.objects.filter(id=id).first()
                    ddl_sql = sql.sql
                    backup_sql = sql.backup_sql
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
                            ddl_sql_list = test.Check(sql=ddl_sql)
                            backup_sql_list = test.Check(sql=backup_sql)

                            return Response({'result': res, 'status': 200})
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return Response({'status': '500'})
