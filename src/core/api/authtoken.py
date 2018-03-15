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
        except KeyError as e:
            print(e)
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            ret_info = '<h1> 访问服务器异常</h1>'
            return HttpResponse(ret_info)
        else:
                if type == 0:  #  审核驳回
                    token = request.GET.get('mytoken')
                    workid = request.GET.get('workid')
                    username = request.GET.get('username')
                    to_user = request.GET.get('to_user')
                    print("===============++++")
                    ret_info = ""
                    try:
                        mail = Account.objects.filter(username=to_user).first()
                        # tag = globalpermissions.objects.filter(authorization='global').first()

                        try:
                            conn = conn_sqlite.query(username, workid)
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
                            reject_remark = '快捷审核驳回，具体驳回原因请联系审核人: '+ mail.email
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
                            data = SqlOrder.objects.filter(work_id=workid).first()
                            tag = globalpermissions.objects.filter(authorization='global').first()
                            content = DatabaseList.objects.filter(id=data.bundle_id).first()
                            SqlOrder.objects.filter(work_id=workid).update(reject=reject_remark)
                            try:
                                print("准备去删除token记录")
                                conn_sqlite.deleteByToken(token)
                                print("删除token记录成功")
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
                                            'to_user': to_user,
                                            # 'to_executor': d.username,
                                            'addr': addr_ip,
                                            'text': data.text,
                                            'type': "审核驳回",
                                            'status': 'approve',
                                            'run_sql': data.sql,
                                            'backup_sql': data.backup_sql,
                                            'token_pass': token,
                                            'rejected': reject_remark,
                                            'myself': username,
                                            'note': content.after}
                                        put_mess = send_email.send_email(to_addr=mail.email)
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
                        username = request.GET.get('username')
                        to_user = request.GET.get('to_user')
                        print("===============++++")
                        ret_info=""
                        try:

                            #tag = globalpermissions.objects.filter(authorization='global').first()

                            try:
                                conn = conn_sqlite.query(username,workid)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info="sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                            if conn:  #如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                                # 执行审核通过的业务
                                SqlOrder.objects.filter(work_id=workid).update(status=1)
                                c = SqlOrder.objects.filter(work_id=workid).first()
                                d = Account.objects.filter(group='executer').first()
                                content = DatabaseList.objects.filter(id=c.bundle_id).first()
                                _tmpData = SqlOrder.objects.filter(work_id=workid).values(
                                    'work_id',
                                    'bundle_id',
                                    'text',
                                ).first()
                                reject_remark = '快捷审核通过，通过原因请联系审核人'
                                title = '工单:' + _tmpData['work_id'] + '审核通过通知'
                                mail = Account.objects.filter(username='dba').first()
                                print(mail.email)
                                msg_content = '工单详情是：' + _tmpData['text'] + '\r\n'
                                Usermessage.objects.get_or_create(
                                    from_user=username,
                                    time=util.date(),
                                    title=title,
                                    content=msg_content,
                                    to_user=to_user,
                                    state='unread'
                                )
                                data = SqlOrder.objects.filter(work_id=workid).first()
                                tag = globalpermissions.objects.filter(authorization='global').first()

                                # ----删除token
                                try:
                                    print("准备去删除token记录")
                                    conn_sqlite.delete(username, workid)
                                    print("删除token记录成功")
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info = "sqlite数据库后台异常，请联系系统管理员"
                                    return HttpResponse(ret_info)

                                # -----增加执行的todken
                                try:
                                    print("准备去增加执行token记录")

                                    conn_sqlite.add_one('dba', data.work_id, newtoken)

                                    print("增加执行token记录成功")
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info = "sqlite数据库后台异常，请联系系统管理员"

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
                                                'status': 'approve',
                                                'run_sql': data.sql,
                                                'backup_sql': data.backup_sql,
                                                'token_pass': newtoken,
                                                'myself': username,
                                                'note': content.after}
                                            put_mess = send_email.send_email(to_addr=mail.email)
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
                        except:
                            ret_info='<h1> 访问服务器异常</h1>'
                            return HttpResponse(ret_info)



        def put(self, request, args=None):
            pass

        def post(self, request, args: str = None):
            pass
