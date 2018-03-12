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
            CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
            print("exception")
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
                        mail = Account.objects.filter(username=username).first()
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
                            reject_remark = '快捷审核驳回，驳回原因请联系审核人'
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

                            # reject_body="<table>" \
                            #            "<tr><td><input type=text></input></td></tr>" \
                            #            "<tr><td><input type=button>确认</input></td></tr>" \
                            #            "<tr><td><input type=button>取消</input></td></tr>" \
                            #            "</table>"

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
                            ret_info = '<h1>审核驳回完成</h1>'
                            return HttpResponse(ret_info)

                        else:  # 不存在token,直接返回异常
                            ret_info = '<h1>您已成功进行审核，无需进行二次操作</h1>'
                            return HttpResponse(ret_info)
                    except:
                        ret_info = '<h1> 访问服务器异常</h1>'
                        return HttpResponse(ret_info)
                elif type == 1:  # 审核通过
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
                                conn = conn_sqlite.query(username,workid)
                            except Exception as e:
                                print(e)
                                CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                ret_info="sqlite数据库后台异常，请联系系统管理员"
                                return HttpResponse(ret_info)

                            if conn:  #如果存在该token，下一步就是直接执行，执行完后还要删除此条数据库token 数据
                                # 执行审核通过的业务
                                SqlOrder.objects.filter(work_id=workid).update(status=1)
                                _tmpData = SqlOrder.objects.filter(work_id=workid).values(
                                    'work_id',
                                    'bundle_id',
                                    'text',
                                ).first()
                                reject_remark = '快捷审核通过，通过原因请联系审核人'
                                title = '工单:' + _tmpData['work_id'] + '审核通过通知'
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


                                # reject_body="<table>" \
                                #            "<tr><td><input type=text></input></td></tr>" \
                                #            "<tr><td><input type=button>确认</input></td></tr>" \
                                #            "<tr><td><input type=button>取消</input></td></tr>" \
                                #            "</table>"

                                # ----删除token
                                try:
                                    print("准备去删除token记录")
                                    conn_sqlite.delete(username, workid)
                                    print("删除token记录成功")
                                except Exception as e:
                                    print(e)
                                    CUSTOM_ERROR.error(f'{e.__class__.__name__}: {e}')
                                    ret_info="sqlite数据库后台异常，请联系系统管理员"
                                    return HttpResponse(ret_info)
                                ret_info = '<h1>恭喜，审核通过完成</h1>'
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
