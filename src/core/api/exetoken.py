import logging
import json
from libs import send_email
from libs import baseview
from libs import util
from libs import conn_sqlite
from rest_framework.response import Response
from django.http import HttpResponse
from core.models import (
    SqlOrder,
    Usermessage,
    DatabaseList,,
    Account,
    globalpermissions
)
conf = util.conf_path()
addr_ip = conf.ipaddress
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

class audit(baseview.Approverpermissions):
    '''
    SQL 执行通过或者执行驳回的方法，通过按钮的URL传参过来
    '''

    def get(self, request, args=None):
        def get(self, request, args=None):
            try:

                type = request.GET.get('type')

            except KeyError as e:
                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                return HttpResponse(status=500)
            else:
                    if type == 0:  # 执行驳回，发送信息和邮件给到审核人
                        try:
                            token = request.GET.get('token')
                            workid = request.GET.get('workid')
                            username = request.GET.get('username')
                            to_user = request.GET.get('to_user')
                        except KeyError as e:
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            return HttpResponse(status=500)
                        else:
                            try:
                                mail = Account.objects.filter(username=username).first()
                                tag = globalpermissions.objects.filter(authorization='global').first()
                                ret_info = '操作成功，该请求已驳回！'
                                query_sql = "select token from  token_db where username=%s and workid=%s" % (
                                username, workid)
                                delete_sql = "delete from token_db where username=%s and workid=%s" % (username, workid)
                                if conn_sqlite.query(query_sql):  # 如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                                    # 执行审核驳回的业务
                                    SqlOrder.objects.filter(id=id).update(status=0)
                                    _tmpData = SqlOrder.objects.filter(id=id).values(
                                        'work_id',
                                        'bundle_id',
                                        'text',
                                    ).first()
                                    reject_remark = '快捷执行驳回，驳回原因请联系审核'
                                    title = '工单:' + _tmpData['work_id'] + '执行驳回通知'
                                    msg_content = '工单详情是：' + _tmpData['text'] + '\r\n 驳回意见是： ' + reject_remark  # 发送短信
                                    Usermessage.objects.get_or_create(
                                        from_user=username,
                                        time=util.date(),
                                        title=title,
                                        content=msg_content,
                                        to_user=to_user,
                                        state='unread'
                                    )
                                    data = SqlOrder.objects.filter(id=id).first()

                                    ret_info = '<h1>恭喜，审核通过完成</h1>'
                                    # reject_body="<table>" \
                                    #            "<tr><td><input type=text></input></td></tr>" \
                                    #            "<tr><td><input type=button>确认</input></td></tr>" \
                                    #            "<tr><td><input type=button>取消</input></td></tr>" \
                                    #            "</table>"
                                    # 发送驳回邮件给到工单发起人
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
                                                    'status': 'back',
                                                    'run_sql': data.sql,
                                                    'backup_sql': data.backup_sql,
                                                    'rejected': reject_remark}
                                                put_mess = send_email.send_email(to_addr=mail.email)
                                                put_mess.send_mail(mail_data=mess_info, type=1)
                                        except:
                                            ret_info = '工单审核驳回成功!但是邮箱推送失败,请查看错误日志排查错误.'
                                    # ----删除token
                                    conn_sqlite.delete(delete_sql)

                                else:  # 不存在token,直接返回异常
                                    ret_info = '<h1> 拒绝访问，按钮操作已失效</h1>'

                            except:
                                ret_info = '<h1> 访问服务器异常</h1>'
                            return Response(ret_info)
                    elif type == 1:  #   执行成功，发送信息和邮件给到工单发起人和审核人
                        token = request.GET.get('token')
                        workid = request.GET.get('workid')
                        username = request.GET.get('username')
                        to_user = request.GET.get('to_user')
                        try:
                            mail = Account.objects.filter(username=username).first()
                            tag = globalpermissions.objects.filter(authorization='global').first()
                            ret_info = '操作成功，该请求已通过！'
                            query_sql = "select token from  token_db where username=%s and workid=%s" % (
                            username, workid)
                            delete_sql = "delete from token_db where username=%s and workid=%s" % (username, workid)
                            if conn_sqlite.query(query_sql):  # 如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                                # 执行审核通过的业务
                                SqlOrder.objects.filter(id=id).update(status=1)

                                _tmpData = SqlOrder.objects.filter(id=id).values(
                                    'work_id',
                                    'bundle_id',
                                    'text',
                                ).first()
                                reject_remark = '快捷审核驳回，驳回原因请联系审核'
                                title = '工单:' + _tmpData['work_id'] + '审核驳回通知'
                                msg_content = '工单详情是：' + _tmpData['text'] + '\r\n 驳回意见是： ' + reject_remark  # 发送短信
                                Usermessage.objects.get_or_create(
                                    from_user=username,
                                    time=util.date(),
                                    title=title,
                                    content=msg_content,
                                    to_user=to_user,
                                    state='unread'
                                )
                                data = SqlOrder.objects.filter(id=id).first()

                                ret_info = '<h1>恭喜，执行成功</h1>'
                                # reject_body="<table>" \
                                #            "<tr><td><input type=text></input></td></tr>" \
                                #            "<tr><td><input type=button>确认</input></td></tr>" \
                                #            "<tr><td><input type=button>取消</input></td></tr>" \
                                #            "</table>"
                                # 发送驳回邮件给到工单发起人
                                if tag is None or tag.email == 0:
                                    pass
                                else:
                                    try:
                                        if mail.email:
                                            mess_info = {
                                                'workid': _tmpData['work_id'],
                                                'to_user': to_user,
                                                'addr': addr_ip,
                                                'type': "执行成功",
                                                'status': 'back',
                                                'run_sql': data.sql,
                                                'backup_sql': data.backup_sql}
                                            put_mess = send_email.send_email(to_addr=mail.email)
                                            put_mess.send_mail(mail_data=mess_info, type=1)
                                    except:
                                        ret_info = '工单执行成功!但是邮箱推送失败,请查看错误日志排查错误.'
                                # ----删除token
                                conn_sqlite.delete(delete_sql)
                                ret_info = '<h1>恭喜，执行成功/h1>'
                            else:  # 不存在token,直接返回异常
                                ret_info = '<h1> 拒绝访问，按钮操作已失效</h1>'
                        except:
                            ret_info = '<h1> 访问服务器异常</h1>'

                        return Response(ret_info)

                    else:
                        pass
