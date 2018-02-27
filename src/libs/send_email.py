from libs import util
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

conf = util.conf_path()
from_addr = conf.mail_user
password = conf.mail_password
smtp_server = conf.smtp


class send_email(object):

    def __init__(self, to_addr=None):
        self.to_addr = to_addr

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_mail(self,mail_data=None,type=None):
        if type == 0: #同意
            text = '<html><body><h1>蜜罐运维 工单同意通知</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>发起人: %s</p>' \
                   '<br><p>地址: <a href="%s">%s</a></p>' \
                   '<br><p>工单备注: %s</p>' \
                   '<br><p>状态: 同意</p>' \
                   '<br><p>备注: %s</p>' \
                   '</body></html>' %(
                mail_data['workid'],
                mail_data['to_user'],
                mail_data['addr'],
                mail_data['addr'],
                mail_data['text'],
                mail_data['note'])
        elif type == 1: #驳回
            text = '<html><body><h1>蜜罐运维 工单驳回通知</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>发起人: %s</p>' \
                   '<br><p>地址: <a href="%s">%s</a></p>' \
                   '<br><p>状态: 驳回</p>' \
                   '<br><p>驳回说明: %s</p>' \
                   '</body></html>' % (
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['addr'],
                       mail_data['addr'],
                       mail_data['rejected'])
        else: #提交                    #'<br><p>请审核人操作: <a href="%s/#/management/management-audit/confirm?id=%s&tokens=%s">同意</a> <br> <a href=''>驳回</a></p>' \
            text = '<html><body><h1>蜜罐运维 工单提交通知</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>发起人: %s</p>' \
                   '<br><p>登录平台: <a href="%s">%s</a></p>' \
                   '<br><p>工单备注: %s</p>' \
                   '<br><p>状态: 已提交</p>' \
                   '<br><p>备注: %s</p>' \
                   '<br><p>请审核人操作: <a href="">&nbsp&nbsp审核通过</a> &nbsp&nbsp&nbsp&nbsp&nbsp <a href=''>审核驳回</a></p>' \
                   '<br><p>使用说明：只要您点击了通过或者驳回，输入您的登录密码即可直接审核工单，而不再需要继续登录平台操作；</p>' \
                   '<br><p>&nbsp&nbsp&nbsp&nbsp&nbsp 同时,工单发起人将会收到审核邮件，以及工单执行人也会收到执行提醒邮件</p>' \
                   '</body></html>' % (
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['addr'],
                       mail_data['addr'],
                       mail_data['text'],
                       #mail_data['addr'],
                       #mail_data['orderID'],
                       #mail_data['tokens'],
                       mail_data['note'])
        msg = MIMEText(text, 'html', 'utf-8')
        msg['From'] = self._format_addr('蜜罐管理员 <%s>' % from_addr)
        msg['To'] = self._format_addr('Dear_guest <%s>' % self.to_addr)
        msg['Subject'] = Header('蜜罐运维-工单消息推送', 'utf-8').encode()

        #server = smtplib.SMTP(smtp_server, 25)
        server = smtplib.SMTP_SSL(smtp_server,port=465)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [self.to_addr], msg.as_string())
        server.quit()

        
