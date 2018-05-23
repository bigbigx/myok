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
# login_url="http://ops.51dinghuo.cc"
login_url="http://127.0.0.1:88"



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
                   '<br><p>工单申请人: %s</p>' \
                   '<br><p>工单申请时间: %s</p>' \
                   '<br><p>工单审核人: %s</p>' \
                   '<br><p>工单审核时间: %s</p>' \
                   '<br><p>机房: %s</p>' \
                   '<br><p>连接名: %s</p>' \
                   '<br><p>数据库: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>受影响的应用系统: %s</p>' \
                   '<br><p>审核状态: 审核通过 </p>' \
                   '<br><p>审核说明: %s </p>' \
                   '<br><p>登录平台: <a href=%s  target="_blank">点击登录</a></p><p></p>' \
                   '<a href="%s/api/v1/exe_token?type=1&apply_man=%s&approve_man=%s&workid=%s&mytoken=%s">执行SQL</a> ' \
                   '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
                   '<br><p>使用说明：只要您点击了 "执行SQL" ，即可直接审核工单，而不再需要继续登录平台操作；' \
                   '<br>&nbsp&nbsp&nbsp&nbsp&nbsp 同时,工单发起人将会收到审核邮件，以及工单执行人也会收到执行提醒邮件</p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['apply_man'],
                       mail_data['apply_time'],
                       mail_data['approve_man'],
                       mail_data['approvetime'],
                       mail_data['computer_room'],
                       mail_data['connection_name'],
                       mail_data['db'],
                       mail_data['backup_sql'],
                       mail_data['run_sql'],
                       mail_data['system'],
                       mail_data['pass_remark'],
                       login_url,
                       login_url,
                       mail_data['apply_man'],
                       mail_data['approve_man'],
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
                   '<br><p>工单申请人: %s</p>' \
                   '<br><p>工单申请时间: %s</p>' \
                   '<br><p>工单审核人: %s</p>' \
                   '<br><p>工单审核时间: %s</p>' \
                   '<br><p>工单执行人: %s</p>' \
                   '<br><p>工单执行时间: %s</p>' \
                   '<br><p>机房: %s</p>' \
                   '<br><p>连接名: %s</p>' \
                   '<br><p>数据库: %s</p>' \
                   '<br><p>受影响的应用系统: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>状态: SQL执行完成 </p>' \
                   '<br><p>说明: 有备份SQL语句,请查看附件excel,执行顺序和附件时间顺序一致，请按顺序编号下载备份数据 </p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['apply_man'],
                       mail_data['apply_time'],
                       mail_data['approve_man'],
                       mail_data['approvetime'],
                       mail_data['execute_man'],
                       mail_data['executetime'],
                       mail_data['computer_room'],
                       mail_data['connection_name'],
                       mail_data['db'],
                       mail_data['system'],
                       mail_data['run_sql'],
                       mail_data['backup_sql']
                       )
            cc_list = mail_data['cc_list']
            print(cc_list)
            cc_address_list = []
            receive_man = []
            if cc_list == [] or cc_list == '[]':
                receive_man = [self.to_addr]  # to and cc
                print(receive_man)
            else:
                cc_address_list = util.myok(cc_list)
                receive_man = [self.to_addr] + cc_address_list
                print(receive_man)

                # approver_mail = mail_data['approve_man']
            # cc_address_list = util.myok(cc_list)
            msg['To'] = self._format_addr('Dear 用户 <%s>' % (self.to_addr))
            msg['Cc'] = self._format_addr('Dear 用户 <%s>' % ','.join(cc_address_list))
            msg['Subject'] = Header('蜜罐工单状态---SQL执行完成', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')
            for i in mail_data['file']:
                    file = MIMEBase('application', 'octet-stream')
                    file.set_payload(open(i, 'rb').read())
                    file.add_header('Content-Disposition', 'attachment', filename=i)
                    encoders.encode_base64(file)
                    _attachments.append(file)
            for att in _attachments:
                msg.attach(att)
            msg.attach(contents)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            # server.sendmail(from_addr, [self.to_addr] + [cc_str], msg.as_string())

            server.sendmail(from_addr, receive_man, msg.as_string())
            # server.sendmail(from_addr, [self.to_addr]+[approver_mail] + cc_address_list, msg.as_string())
            server.quit()


        elif type == 1:  # 审核驳回，邮件发送到工单发起人，而且不允许邮件再次发起，必须通过平台重新发起
            text = '<html><body><h1>工单标题：%s</h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>机房: %s</p>' \
                   '<br><p>连接名: %s</p>' \
                   '<br><p>数据库: %s</p>' \
                   '<br><p>受影响的应用系统: %s</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>状态: 审核驳回 (注意：请登录平台进行sql调整)</p>' \
                   '<br><p>驳回说明: %s</p>' \
                   '<br><p>登录平台: <a href="http://ops.51dinghuo.cc"  target="_blank">点击登录</a></p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['apply_man'],
                       mail_data['computer_room'],
                       mail_data['connection_name'],
                       mail_data['db'],
                       mail_data['system'],
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
                       mail_data['apply_man'],
                       mail_data['rejected'])
            msg['To'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
            msg['Subject'] = Header('蜜罐工单状态---SQL执行驳回', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')
            msg.attach(contents)
            # server = smtplib.SMTP(smtp_server, 25)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            print([self.to_addr])
            # server.sendmail(from_addr, [self.to_addr] + cc_list, msg.as_string())
            server.sendmail(from_addr, [self.to_addr], msg.as_string())
            server.quit()

        else:  # 提交成功，邮件只发送到审核人,抄送到相关人员
            cc_list = mail_data['cc_list']
            text = '<html><body><h1> 工单标题：%s  </h1>' \
                   '<br><p>工单号: %s</p>' \
                   '<br><p>工单发起人: %s</p>' \
                   '<br><p>机房: %s</p>' \
                   '<br><p>连接名: %s</p>' \
                   '<br><p>数据库: %s</p>' \
                   '<br><p>受影响的应用系统: %s</p>' \
                   '<br><p>状态: 成功申请工单</p>' \
                   '<br><p>执行SQL: %s</p>' \
                   '<br><p>备份SQL: %s</p>' \
                   '<br><p>登录平台: <a href=%s  target="_blank">点击登录</a></p>' \
                   '<br><p>请审核人操作: (注意：点击审核同意，不会马上执行SQL) &nbsp&nbsp' \
                   '<a href="%s/api/v1/audit_token?type=1&db=%s&apply_man=%s&approve_man=%s&workid=%s&mytoken=%s">审核通过</a> ' \
                   '&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp ' \
                   '<a href="%s/api/v1/audit_token?&type=0&db=%s&apply_man=%s&approve_man=%s&workid=%s&mytoken=%s">审核驳回</a></p>' \
                   '<br><p>使用说明：只要您点击了 "审核通过" 或者 "审核驳回" ，即可直接审核工单，而不再需要继续登录平台操作；' \
                   '<br>&nbsp&nbsp&nbsp&nbsp&nbsp 同时,工单发起人将会收到审核邮件，以及工单执行人也会收到执行提醒邮件</p>' \
                   '</body></html>' % (
                       mail_data['text'],
                       mail_data['workid'],
                       mail_data['apply_man'],
                       mail_data['computer_room'],
                       mail_data['connection_name'],
                       mail_data['db'],
                       mail_data['system'],
                       mail_data['run_sql'],
                       mail_data['backup_sql'],
                       # mail_data['addr'],
                       # mail_data['orderID'],
                       # mail_data['tokens'],
                       login_url,
                       login_url,
                       mail_data['db'],
                       mail_data['apply_man'],
                       mail_data['approve_man'],
                       mail_data['workid'],
                       mail_data['token_pass'],
                       login_url,
                       mail_data['db'],
                       mail_data['apply_man'],
                       mail_data['approve_man'],
                       mail_data['workid'],
                       mail_data['token_reject'])

            # cc_text = '<html><body><h1>工单标题：%s</h1>' \
            #        '<br><p>工单号: %s</p>' \
            #        '<br><p>工单发起人: %s</p>' \
            #        '<br><p>数据库: %s</p>' \
            #        '<br><p>执行SQL: %s</p>' \
            #        '<br><p>备份SQL: %s</p>' \
            #        '<br><p>受影响的应用系统: %s</p>' \
            #        '<br><p>状态: 成功申请工单,等待审核和执行</p>' \
            #        '</body></html>' % (
            #            mail_data['text'],
            #            mail_data['workid'],
            #            mail_data['apply_man'],
            #            mail_data['db'],
            #            mail_data['run_sql'],
            #            mail_data['backup_sql'],
            #            mail_data['system'],
            #            )
            msg['To'] = self._format_addr('Dear 用户 <%s>' % self.to_addr)
            msg['Subject'] = Header('蜜罐工单状态---SQL成功申请', 'utf-8').encode()
            contents = MIMEText(text, 'html', 'utf-8')
            msg.attach(contents)
            server = smtplib.SMTP_SSL(smtp_server, port=465)
            server.set_debuglevel(1)
            server.login(from_addr, password)
            server.sendmail(from_addr, [self.to_addr], msg.as_string())
            server.quit()

            # mail to cc person:
