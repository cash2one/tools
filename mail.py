#!/usr/bin/python
# coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.Header import Header
from email.mime.multipart import MIMEMultipart

mailfrom = 
mailto = 
mailuser = 
mailpasswd = 
mailaddr = 
mailport = '25'

class mail:
    def __init__(self, environment, url):
        
        self.environment = environment
        
        self.url = url
        
        self.mail = smtplib.SMTP()
        self.msg = MIMEMultipart()

    def conn(self, mailaddr, mailport = '25'):
        self.mail.connect(mailaddr, mailport)

    def login(self, mailuser = mailfrom, mailpasswd = ''):
        self.mail.login(mailuser, mailpasswd)

    def makemsg(self):
        self.msg['From'] = mailfrom
        self.msg['To'] = mailto

    
    
        urlist = self.url.replace('___', '\n').replace('__', '\t')

        self.msg['Subject'] = Header('[运维统计]**  %s url加载速度排行: **' % (self.environment), charset = 'UTF-8')
        content = MIMEText("** 取50次平均时间 **\n\n \
        Environment: %s\n \
        \n %s \n " % (self.environment, urlist), _subtype='plain', _charset='UTF-8')

        self.msg.attach(content)

    def send(self, mailto):
        self.mail.sendmail(mailfrom, mailto, self.msg.as_string())

    def close(self):
        self.mail.quit()

def main():
    import getopt, sys
    opts, args = getopt.getopt(sys.argv[1:], 'e:u:t:',
                               ['environment=', 'url=', 'mailto='])

    for opt, arg in opts:

        # 环境
        if opt in ('-e', 'environment'):
            environment = arg
        # 验证失败URL
        if opt in ('-u', 'url'):
            url = arg
        #发送人
        if opt in ('-t', 'mailto'):
            mailto = arg

    report = mail(environment, url)
    report.conn(mailaddr, mailport)
    report.login(mailuser, mailpasswd)
    report.makemsg()
    for line in mailto.split(','):
        print 'send',
        report.send(line)
        print 'complete'
    report.close()

if __name__ == '__main__':
    main()
