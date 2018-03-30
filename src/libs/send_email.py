from libs import util
from email.header import Header
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.utils import parseaddr, formataddr
import smtplib
# from libs.readfile import readfile

conf = util.conf_path()
from_addr = conf.mail_user
password = conf.mail_password
smtp_server = conf.smtp
login_url="http://ops.51dinghuo.cc"
# login_url="http://127.0.0.1:88"



class send_email(object):

    def __init__(self, to_addr=None):
        self.to_addr = to_addr

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def send_mail(self, mail_data=None, type=None):
        _attachments = []
        msg = MIMEMultipart('alternative')
        msg['From'] = self._format_addr('蜜罐管理员 <%s>' % from_addr)


        # msg['Subject'] = Header('蜜罐运维-工单消息推送', 'utf-8').encode()

        if type == 0:  # 审核同意，同意后邮件只发送到工单执行人
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>状态: 审核通过 </p>' \
                   '<br><p>备注: %s</p>' \
                   '<br><p>登录平台: <a href=%s  target="_blank">点击登录</a></p><p></p>' \
                   '<a href="%s/api/v1/exe_token?type=1&to_user=%s&username=%s&workid=%s&mytoken=%s">执行SQL</a> ' \
                   '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
                   '<br><p>使用说明：只要您点击了 "执行SQL" ，即可直接审核工单，而不再需要继续登录平台操作；' \
                   '<br>&nbsp&nbsp&nbsp&nbsp&nbsp 同时,工单发起人将会收到审核邮件，以及工单执行人也会收到执行提醒邮件</p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['run_sql'],
                       mail_data['backup_sql'],
                       mail_data['note'],
                       login_url,
                       login_url,
                       mail_data['to_user'],
                       mail_data['myself'],
                       mail_data['workid'],
                       mail_data['token_pass'])
            msg['To'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
            msg['Subject'] = Header('蜜罐工单状态---SQL审核通过', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')

            msg.attach(contents)
            # server = smtplib.SMTP(smtp_server, 25)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            # server.sendmail(from_addr, [self.to_addr] + cc_list, msg.as_string())
            server.sendmail(from_addr, [self.to_addr], msg.as_string())
            server.quit()

        elif type == 3:  # 执行成功，邮件发送到工单发起人和工单审核人
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['run_sql'],
                       mail_data['backup_sql'])
            cc_list = mail_data['cc_list']
            approver_mail = mail_data['approve_man']
            cc_address_list = util.myok(cc_list)
            msg['To'] = self._format_addr('Dear 用户 <%s> <%s>' % (self.to_addr,approver_mail))
            msg['Cc'] = self._format_addr('Dear 用户 <%s>' % ','.join(cc_list))
            msg['Subject'] = Header('蜜罐工单状态---SQL执行完成', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')
            for i in mail_data['file']:
                    file = MIMEBase('application', 'octet-stream')
                    file.set_payload(open(i, 'rb').read())
                    file.add_header('Content-Disposition', 'attachment', filename=i)
                    encoders.encode_base64(file)
                    _attachments.append(file)

            msg.attach(contents)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            if cc_address_list==['']:
                print(1)
                server.sendmail(from_addr, [self.to_addr] + [approver_mail], msg.as_string())
            else:
                print(2)
                server.sendmail(from_addr, [self.to_addr] + [approver_mail] + cc_address_list, msg.as_string())
            # server.sendmail(from_addr, [self.to_addr]+[approver_mail] + cc_address_list, msg.as_string())
            server.quit()


        elif type == 1:  # 审核驳回，邮件发送到工单发起人，而且不允许邮件再次发起，必须通过平台重新发起
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
            msg['To'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
            msg['Subject'] = Header('蜜罐运维工单状态反馈---SQL审核驳回', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')
            msg.attach(contents)
            # server = smtplib.SMTP(smtp_server, 25)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            # server.sendmail(from_addr, [self.to_addr] + cc_list, msg.as_string())
            server.sendmail(from_addr, [self.to_addr], msg.as_string())
            server.quit()
        elif type == 4:  # 执行驳回 邮件发送到工单审核人
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
            msg['To'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
            msg['Subject'] = Header('蜜罐工单状态---SQL执行驳回', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')
            msg.attach(contents)
            # server = smtplib.SMTP(smtp_server, 25)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            # server.sendmail(from_addr, [self.to_addr] + cc_list, msg.as_string())
            server.sendmail(from_addr, [self.to_addr], msg.as_string())
            server.quit()

        else:  # 提交成功，邮件只发送到审核人
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>状态: 成功发起</p>' \
                   '<br><p>备注: %s</p>' \
                   '<br><p>登录平台: <a href=%s  target="_blank">点击登录</a></p>' \
                   '<br><p>请审核人操作: &nbsp&nbsp' \
                   '<a href="%s/api/v1/audit_token?type=1&to_user=%s&username=%s&workid=%s&mytoken=%s">审核通过</a> ' \
                   '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
                   '<a href="%s/api/v1/audit_token?&type=0&to_user=%s&username=%s&workid=%s&mytoken=%s">审核驳回</a></p>' \
                   '<br><p>使用说明：只要您点击了 "审核通过" 或者 "审核驳回" ，即可直接审核工单，而不再需要继续登录平台操作；' \
                   '<br>&nbsp&nbsp&nbsp&nbsp&nbsp 同时,工单发起人将会收到审核邮件，以及工单执行人也会收到执行提醒邮件</p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['to_user'],
                       mail_data['run_sql'],
                       mail_data['backup_sql'],
                       # mail_data['addr'],
                       # mail_data['orderID'],
                       # mail_data['tokens'],
                       mail_data['note'],
                       login_url,
                       login_url,
                       mail_data['to_user'],
                       mail_data['assigned'],
                       mail_data['workid'],
                       mail_data['token_pass'],
                       login_url,
                       mail_data['to_user'],
                       mail_data['assigned'],
                       mail_data['workid'],
                       mail_data['token_reject'])
            msg['To'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
            msg['Subject'] = Header('蜜罐工单状态---SQL成功申请', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')
            msg.attach(contents)
            # server = smtplib.SMTP(smtp_server, 25)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            # server.sendmail(from_addr, [self.to_addr] + cc_list, msg.as_string())
            server.sendmail(from_addr, [self.to_addr], msg.as_string())
            server.quit()
