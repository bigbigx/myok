import logging
import json
from libs import send_email
from libs import baseview
from libs import util
from libs import call_inception
from libs import rollback
from lib import exportexcel
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


#class execute(baseview.SuperUserpermissions):
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
                #pagenumber = SqlOrder.objects.filter(assigned=username).aggregate(alter_number=Count('id'))
                pagenumber = SqlOrder.objects.filter(status=1).aggregate(alter_number=Count('id'))
                start = (int(page) - 1) * 20
                end = int(page) * 20
                    #'''
                    #select core_sqlorder.*,core_databaselist.connection_name, \
                    #core_databaselist.computer_room from core_sqlorder \
                    #INNER JOIN core_databaselist on \
                    #core_sqlorder.bundle_id = core_databaselist.id where core_sqlorder.assigned = '%s' and core_sqlorder.status=1 \
                    #ORDER BY core_sqlorder.id desc
                    #'''%username
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

    ###执行提交
    def put(self, request, args=None):
        try:
            type = request.data['type']
        except KeyError as e:
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
        else:
            if type == 0:  #执行驳回
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
                        #SqlOrder.objects.filter(id=id).update(status=0)
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
                                        %(_tmpData['work_id'],to_user,addr_ip,text), url=content.url)
                            except:
                                ret_info = '工单执行驳回成功!但是钉钉推送失败,请查看错误日志排查错误.'
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
                                        'rejected': text}
                                    put_mess = send_email.send_email(to_addr=mail.email)
                                    put_mess.send_mail(mail_data=mess_info,type=1)
                            except:
                                ret_info = '工单执行驳回成功!但是邮箱推送失败,请查看错误日志排查错误.'
                        return Response(ret_info)
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)

            elif type == 1:  ##执行通过
                try:
                    from_user = request.data['from_user']
                    to_user = request.data['to_user']
                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        SqlOrder.objects.filter(id=id).update(status=4)
                        c = SqlOrder.objects.filter(id=id).first()
                        title = f'工单:{c.work_id}执行成功通知'
                        '''
                        根据工单编号拿出对应sql的拆解数据
                     '''
                        SQL_LIST = DatabaseList.objects.filter(id=c.bundle_id).first()
                        '''
                        发送sql语句到inception中执行
                     '''
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
                            '''
                            修改该工单编号的state状态 ---修改为执行成功状态
                        '''
                            SqlOrder.objects.filter(id=id).update(status=4)
                            # 同时修改时间戳
                            cur_time=int(time.time())
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
                                    person=c.username,
                                    #reviewer=c.assigned,
                                    reviewer=from_user,
                                    affectrow=i['affected_rows'],
                                    sequence=i['sequence'],
                                    backup_dbname=i['backup_dbname'],
                                    # execute_time=i['execute_time']
                                )
                        '''
                        通知消息
                        '''
                        Usermessage.objects.get_or_create(
                            from_user=from_user, time=util.date(),
                            #title=title, content='该工单已执行成功!', to_user=to_user,
                            title=title, content=f'该工单已执行成功！ 工单说明是: {c.text}', to_user=to_user,
                            state='unread'
                        )

                        '''
                        Dingding
                        '''

                        content = DatabaseList.objects.filter(id=c.bundle_id).first()
                        mail = Account.objects.filter(username=to_user).first()
                        tag = globalpermissions.objects.filter(authorization='global').first()
                        ret_info = '操作成功，该执行请求已经完成!并且已在相应库执行！详细执行信息请前往执行记录页面查看！'

                        if tag is None or tag.dingding == 0:
                            pass
                        else:
                            try:
                                if content.url:
                                    util.dingding(
                                        content='工单执行成功通知\n工单编号:%s\n发起人:%s\n地址:%s\n工单备注:%s\n状态:同意\n备注:%s'
                                                          %(c.work_id,c.username,addr_ip,c.text,content.after), url=content.url)


                            except:
                                ret_info = '工单执行成功!但是钉钉推送失败,请查看错误日志排查错误.'

                        if tag is None or tag.email == 0:
                            pass
                        else:
                            try:
                                if mail.email:
                                    mess_info = {
                                        'workid':c.work_id,
                                        'to_user':c.username,
                                        'addr': addr_ip,
                                        'text':c.text,
                                        'type': "执行成功",
                                        'note': content.after}
                                    put_mess = send_email.send_email(to_addr=mail.email)
                                    put_mess.send_mail(mail_data=mess_info,type=0)
                            except:
                                ret_info = '工单执行成功!但是邮箱推送失败,请查看错误日志排查错误.'
                        return Response(ret_info)
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)


            elif type =='backup':  ##执行前备份
                try:
                    from_user = request.data['from_user']
                    to_user = request.data['to_user']
                    id = request.data['id']
                except KeyError as e:
                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                    return HttpResponse(status=500)
                else:
                    try:
                        SqlOrder.objects.filter(id=id).update(status=6)
                        title = f'工单:{c.work_id}SQL备份成功通知'

                        c = exportexcel.toExcel(
                            Host=ip,
                            User=user,
                            Password=password,
                            Database=db,
                            Charset='utf8')
                        a = c.exportTables(Conn=connection_name, Schemal=basename, TableList=data)
                        return Response(
                            {
                                'status': 'excel文档已生成',
                                'url': '%s_%s_Dictionary_%s.cvs' % (connection_name, basename, a)
                            }
                        )
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)

                        '''
                        通知消息
                        '''
                        Usermessage.objects.get_or_create(
                            from_user=from_user, time=util.date(),
                            #title=title, content='该工单已执行成功!', to_user=to_user,
                            title=title, content=f'该工单已备份成功! 备份附件请查看邮件 ！   工单说明: {c.text}', to_user=to_user,
                            state='unread'
                        )

                        '''
                        Dingding
                        '''

                        content = DatabaseList.objects.filter(id=c.bundle_id).first()
                        mail = Account.objects.filter(username=to_user).first()
                        tag = globalpermissions.objects.filter(authorization='global').first()
                        ret_info = '备份成功，该备份请求已经完成!并且已在相应库执行！详细备份信息请前往邮件查看！'

                        if tag is None or tag.dingding == 0:
                            pass
                        else:
                            try:
                                if content.url:
                                    util.dingding(
                                        content='工单SQL备份成功通知\n工单编号:%s\n发起人:%s\n地址:%s\n工单备注:%s\n状态:同意\n备注:%s'
                                                          %(c.work_id,c.username,addr_ip,c.text,content.after), url=content.url)


                            except:
                                ret_info = '工单SQL备份成功!但是钉钉推送失败,请查看错误日志排查错误.'

                        if tag is None or tag.email == 0:
                            pass
                        else:
                            try:
                                if mail.email:
                                    mess_info = {
                                        'workid':c.work_id,
                                        'to_user':c.username,
                                        'addr': addr_ip,
                                        'text':c.text,
                                        'type': "备份成功",
                                        'note': content.after}
                                    put_mess = send_email.send_email(to_addr=mail.email)
                                    put_mess.send_mail(mail_data=mess_info,type=0)
                            except:
                                ret_info = '工单SQL备份成功!但是邮箱推送失败,请查看错误日志排查错误.'
                        return Response(ret_info)
                    except Exception as e:
                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                        return HttpResponse(status=500)


            elif type == 'test':  ## 含ddl & dml检测和sql备份语句显示
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
