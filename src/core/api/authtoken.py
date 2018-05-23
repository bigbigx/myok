# -*- coding=utf-8 -*-
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
    DatabaseList,
    Account,
    globalpermissions
)
import datetime
conf = util.conf_path()
addr_ip = conf.ipaddress
CUSTOM_ERROR = logging.getLogger('Yearning.core.views')

class authtoken(baseview.AnyLogin):
    '''
    SQL审核通过或者审核驳回的方法，通过按钮的URL传参过来
    '''
    def get(self, request, args=None):
        try:

            type = int(request.GET.get('type'))
            apply_man = request.GET.get('apply_man') # 发起人
            approve_man = request.GET.get('approve_man') # 审核人
            basename = request.GET.get('db')
            execute_man = 'dba'  #执行人
            execute_group= 'executer'
            cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            ret_info = '<h1> 访问服务器异常</h1>'
            return HttpResponse(ret_info)
        else:
                if type == 0:  #  审核驳回
                    token = request.GET.get('mytoken')
                    workid = request.GET.get('workid')
                    print("===============++++")
                    ret_info = ""
                    try:
                        mail_approve_man = Account.objects.filter(username=approve_man).first()
                        mail_apply_man = Account.objects.filter(username=apply_man).first()
                        # tag = globalpermissions.objects.filter(authorization='global').first()

                        try:
                            conn = conn_sqlite.query(apply_man, workid)
                        except Exception as e:
                            print(e)
                            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                            ret_info = "sqlite数据库后台异常，请联系系统管理员"
                            return HttpResponse(ret_info)

                        if conn:  # 如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                            # 执行审核驳回的业务
                            SqlOrder.objects.filter(work_id=workid).update(status=0)
                            _tmpData = SqlOrder.objects.filter(work_id=workid).values(
                                'work_id',
                                'bundle_id',
                                'text',
                            ).first()
                            reject_remark = '邮件审核驳回，具体驳回原因请联系审核人: '+ mail_approve_man.email
                            title = '工单:' + _tmpData['work_id'] + '审核驳回通知'
                            msg_content = '工单详情是：' + _tmpData['text'] + '\r\n 驳回意见是： ' + reject_remark  # 发送短信
                            Usermessage.objects.get_or_create(
                                from_user=approve_man,
                                time=util.date(),
                                title=title,
                                content=msg_content,
                                to_user=apply_man,
                                state='unread'
                            )
                            data = SqlOrder.objects.filter(work_id=workid).first()
                            tag = globalpermissions.objects.filter(authorization='global').first()
                            content = DatabaseList.objects.filter(id=data.bundle_id).first()
                            SqlOrder.objects.filter(work_id=workid).update(reject=reject_remark)
                            SqlOrder.objects.filter(work_id=workid).update(approvetime=cur_time)  # 记录审核驳回时间
                            try:
                                conn_sqlite.deleteByToken(token)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info = "sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                            if tag is None or tag.email == 0:
                                pass
                            else:
                                try:
                                    if mail_apply_man.email:
                                        mess_info = {
                                            'workid': workid,
                                            'apply_man': apply_man,
                                            # 'to_executor': d.username,
                                            'addr': addr_ip,
                                            'text': data.text,
                                            'type': "审核驳回",
                                            'status': 'approve',
                                            'run_sql': data.sql,
                                            'backup_sql': data.backup_sql,
                                            'token_pass': token,
                                            'rejected': reject_remark,
                                            'db': basename,
                                            'approve_man': approve_man,
                                            'note': content.after}
                                        put_mess = send_email.send_email(to_addr=mail_apply_man.email)
                                        put_mess.send_mail(mail_data=mess_info, type=1)
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info = '工单审核通过!但是邮箱推送失败,请查看错误日志排查错误.'
                                    return HttpResponse(ret_info)

                            ret_info = '<h1>已驳回</h1>'
                            return HttpResponse(ret_info)

                        else:  # 不存在token,直接返回异常
                            ret_info = '<h1>您已成功进行审核，无需进行二次操作</h1>'
                            return HttpResponse(ret_info)
                    except:
                        ret_info = '<h1> 访问服务器异常</h1>'
                        return HttpResponse(ret_info)
                elif type == 1:  # 审核通过
                        token = request.GET.get('mytoken')
                        newtoken = util.generateTokens(32)
                        workid = request.GET.get('workid')
                        ret_info=""
                        try:
                            #tag = globalpermissions.objects.filter(authorization='global').first()
                            try:
                                conn = conn_sqlite.query(approve_man, workid)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info="sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                            if conn:  #如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                                # 执行审核通过的业务
                                SqlOrder.objects.filter(work_id=workid).update(status=1)
                                # SqlOrder.objects.filter(work_id=workid).update(approve_time=cur_time)
                                c = SqlOrder.objects.filter(work_id=workid).first()
                                d = Account.objects.filter(group=execute_group).first()
                                content = DatabaseList.objects.filter(id=c.bundle_id).first()
                                _tmpData = SqlOrder.objects.filter(work_id=workid).values(
                                    'work_id',
                                    'bundle_id',
                                    'text',
                                ).first()
                                pass_remark = '邮件审核通过，通过原因请联系审核人'
                                title = '工单:' + _tmpData['work_id'] + '审核通过通知'
                                execute_man_mail = Account.objects.filter(username=execute_man).first()
                                msg_content = '工单详情是：' + _tmpData['text'] + '\r\n'
                                Usermessage.objects.get_or_create(
                                    from_user=approve_man,
                                    time=util.date(),
                                    title=title,
                                    content=msg_content,
                                    to_user=apply_man,
                                    state='unread'
                                )
                                data = SqlOrder.objects.filter(work_id=workid).first()
                                tag = globalpermissions.objects.filter(authorization='global').first()
                                SqlOrder.objects.filter(work_id=workid).update(approvetime=cur_time)  # 记录审核通过时间
                                SqlOrder.objects.filter(id=id).update(reject=pass_remark)  # 记录审核同意的备注
                                # ----删除token
                                try:
                                    conn_sqlite.delete(approve_man, workid)
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info = "sqlite数据库后台异常，请联系系统管理员"
                                    return HttpResponse(ret_info)

                                # -----增加执行的todken
                                try:

                                    conn_sqlite.add_one(execute_man, data.work_id, newtoken)

                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info = "sqlite数据库后台异常，请联系系统管理员"

                                if tag is None or tag.email == 0:
                                    pass
                                else:
                                    try:
                                        if execute_man_mail.email:
                                            mess_info = {
                                                'workid': workid,
                                                'execute_man': execute_man,
                                                #'to_executor': d.username,
                                                'addr': addr_ip,
                                                'text': c.text,
                                                'type': "审核成功",
                                                'status': 'approve',
                                                'run_sql': data.sql,
                                                'backup_sql': data.backup_sql,
                                                'approvetime': c.approvetime,
                                                'pass_remark': pass_remark,
                                                'system': c.system,
                                                'token_pass': newtoken,
                                                'db': basename,
                                                'approve_man': approve_man,
                                                'apply_man': apply_man,
                                                'note': content.after}
                                            put_mess = send_email.send_email(to_addr=execute_man_mail.email)
                                            put_mess.send_mail(mail_data=mess_info, type=0)
                                    except Exception as e:
                                        print(e)
                                        CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                        ret_info = '工单审核通过!但是邮箱推送失败,请查看错误日志排查错误.'
                                        return HttpResponse(ret_info)


                                ret_info = '<h1>已审核</h1>'
                                return HttpResponse(ret_info)



                            else:  #不存在token,直接返回异常
                                ret_info='<h1>您已成功进行审核，无需进行二次操作</h1>'
                                return HttpResponse(ret_info)
                        except Exception as e:
                            print(e)
                            ret_info='<h1> 访问服务器异常</h1>'
                            return HttpResponse(ret_info)



        def put(self, request, args=None):
            pass

        def post(self, request, args: str = None):
            pass
