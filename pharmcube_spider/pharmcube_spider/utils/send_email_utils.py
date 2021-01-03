# coding: utf-8

import logging
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# https://blog.csdn.net/winter199/article/details/90081078
class SendEmail:
    def __init__(self):
        self.smtpserver = 'smtp.exmail.qq.com'
        self.username = 'zengxiangxu@pharmcube.com'
        self.password = 'Zxx13225853579'
        self.sender = 'zengxiangxu@pharmcube.com'
    '''
      :param content: 含html标签的文本内容
      :param receiver: 收件人可以是多个（数组）
    '''
    def send_email_content(self, content, receiver, subject):
        if len(receiver) < 1:
            logging.error(f'------- 当前发送邮件人数为0，邮件停止发送：{subject} -------')
            return
        logging.info(f'发送邮件：{subject}')
        subject = Header(subject, 'utf-8').encode()
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = self.sender
        # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
        msg['To'] = ";".join(receiver)
        text_html = MIMEText(content, 'html', 'utf-8')
        #附件的形式
        #text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
        msg.attach(text_html)
        smtp = smtplib.SMTP()
        smtp.connect(self.smtpserver)
        # smtp.set_debuglevel(1)# 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, receiver, msg.as_string())
        smtp.quit()

#SendEmail().send_email_content(content=content,receiver=['zengxiangxu@pharmcube.com'],subject='python3 send email test')