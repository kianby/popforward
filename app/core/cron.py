#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import smtplib
import poplib
from email.mime.text import MIMEText
from conf import config

logger = logging.getLogger(__name__)


def fetchforward():
    M = poplib.POP3(config.get(config.POP3_HOST))
    M.user(config.get(config.POP3_LOGIN))
    M.pass_(config.get(config.POP3_PASSWORD))
    numMessages = len(M.list()[1])
    for i in range(numMessages):
        (_, body, _) = M.retr(i + 1)
        message = b"\n".join(body)
        mail(message)
        r = M.dele(i+1)
        logger.info(r)
    M.quit()

def pop():
    try:
       fetchforward() 
    except:
        logger.exception("erreur traitement")
        mail_error("")

    
def mail_error(ex):
    msg = MIMEText(ex)
    msg["Subject"] = "POP FORWARD EXCEPTION"
    msg["To"] = config.get(config.SMTP_TO)
    msg["From"] = config.get(config.SMTP_LOGIN)

    s = smtplib.SMTP(config.get(config.SMTP_HOST), config.getInt(config.SMTP_PORT))
    if config.getBool(config.SMTP_STARTTLS):
        s.starttls()
    s.login(config.get(config.SMTP_LOGIN), config.get(config.SMTP_PASSWORD))
    s.sendmail(config.get(config.SMTP_LOGIN), config.get(config.SMTP_TO), msg)
    s.quit()

def mail(message):
    s = smtplib.SMTP(config.get(config.SMTP_HOST), config.getInt(config.SMTP_PORT))
    if config.getBool(config.SMTP_STARTTLS):
        s.starttls()
    s.login(config.get(config.SMTP_LOGIN), config.get(config.SMTP_PASSWORD))
    s.sendmail(config.get(config.SMTP_LOGIN), config.get(config.SMTP_TO), message)
    s.quit()
