from libs import util
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
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
        if type == 0: #含审核通过，工单发送到工单发起人和工单审核人
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>状态: 审核通过 </p>' \
                   '<br><p>备注: %s</p>' \
                   '<br><p>登录平台: <a href="http://ops.51dinghuo.cc"  target="_blank">点击登录</a></p><p></p>' \
                   '<a href="http://ops.51dinghuo.cc/api/v1/exe_token?type=1&to_user=%s&username=%s&workid=%s&mytoken=%s">执行SQL</a> ' \
                   '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
                   '<br><p>使用说明：只要您点击了 "执行SQL" ，即可直接审核工单，而不再需要继续登录平台操作；' \
                   '<br>&nbsp&nbsp&nbsp&nbsp&nbsp 同时,工单发起人将会收到审核邮件，以及工单执行人也会收到执行提醒邮件</p>' \
                   '</body></html>' %(
                mail_data['text'],
                mail_data['workid'],
                mail_data['to_user'],
                mail_data['run_sql'],
                mail_data['backup_sql'],
                mail_data['note'],
                mail_data['to_user'],
                mail_data['myself'],
                mail_data['workid'],
                mail_data['token_pass'])

        elif type == 3: #执行成功，邮件发送到工单发起人和工单审核
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>状态: %s %s</p>' \
                   '<br><p>备注: %s  </p>' \
                   '<br><p>登录平台: <a href="http://ops.51dinghuo.cc"  target="_blank">点击登录</a></p>' \
                   '</body></html>' %(
                mail_data['text'],
                mail_data['workid'],
                mail_data['to_user'],
                mail_data['run_sql'],
                mail_data['backup_sql'],
                mail_data['backup'],
                mail_data['type'],
                mail_data['note'])


        elif type == 1: #审核驳回，邮件发送到工单发起人，而且不允许邮件再次发起，必须通过平台重新发起
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>状态: 审核驳回 (注意：请登录平台进行sql调整)</p>' \
                   '<br><p>驳回说明: %s</p>' \
                   '<br><p>登录平台: <a href="http://ops.51dinghuo.cc"  target="_blank">点击登录</a></p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['run_sql'],
                       mail_data['backup_sql'],
                       mail_data['rejected'])
        elif type == 4: #执行驳回 邮件发送到工单审核人
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>状态: 执行驳回</p>' \
                   '<br><p>驳回说明: %s</p>' \
                   '<br><p>登录平台: <a href="http://ops.51dinghuo.cc"  target="_blank">点击登录</a></p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['rejected'])

        else: # 提交成功，邮件发送到审核人  # '<br><p>请审核人操作: <a href="%s/#/management/management-audit/confirm?id=%s&tokens=%s">同意</a> <br> <a href=''>驳回</a></p>' \
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>状态: 成功发起</p>' \
                   '<br><p>备注: %s</p>' \
                   '<br><p>登录平台: <a href="http://ops.51dinghuo.cc"  target="_blank">点击登录</a></p>' \
                   '<br><p>请审核人操作: &nbsp&nbsp' \
                   '<a href="http://ops.51dinghuo.cc/api/v1/audit_token?type=1&to_user=%s&username=%s&workid=%s&mytoken=%s">审核通过</a> ' \
                   '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
                   '<a href="http://ops.51dinghuo.cc/api/v1/audit_token?&type=0&to_user=%s&username=%s&workid=%s&mytoken=%s">审核驳回</a></p>' \
                   '<br><p>使用说明：只要您点击了 "审核通过" 或者 "审核驳回" ，即可直接审核工单，而不再需要继续登录平台操作；' \
                   '<br>&nbsp&nbsp&nbsp&nbsp&nbsp 同时,工单发起人将会收到审核邮件，以及工单执行人也会收到执行提醒邮件</p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['run_sql'],
                       mail_data['backup_sql'],
                       #mail_data['addr'],
                       #mail_data['orderID'],
                       #mail_data['tokens'],
                       mail_data['note'],
                       mail_data['to_user'],
                       mail_data['assigned'],
                       mail_data['workid'],
                       mail_data['token_pass'],
                       mail_data['to_user'],
                       mail_data['assigned'],
                       mail_data['workid'],
                       mail_data['token_reject']
            )
        _attachments = []
        msg = MIMEMultipart('alternative')
        contents = MIMEText(text, 'html', 'utf-8')
        msg['From'] = self._format_addr('蜜罐管理员 <%s>' % from_addr)
        msg['To'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
        msg['Cc'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
        msg['Subject'] = Header('蜜罐运维-工单消息推送', 'utf-8').encode()


        if (mail_data['status'] == 'run'):
            for i in mail_data['file']:
               file = MIMEBase('application', 'octet-stream')
               file.set_payload(open(i, 'rb').read())
               file.add_header('Content-Disposition', 'attachment', filename=i)
               encoders.encode_base64(file)
               _attachments.append(file)
            for att in _attachments:
                msg.attach(att)
        else:
            pass

        msg.attach(contents)
        #server = smtplib.SMTP(smtp_server, 25)
        server = smtplib.SMTP_SSL(smtp_server,port=465)
        server.set_debuglevel(1)
        server.login(from_addr, password)
        self.to_addr = self.to_addr+'liaojun@zskuaixiao.com'
        server.sendmail(from_addr, [self.to_addr], msg.as_string())
        server.quit()

        
