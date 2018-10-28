#!/usr/bin/env python
# -*- coding: utf-8 -*-

import profig

POP3_POLLING = "pop3.polling"
POP3_SSL = "pop3.ssl"
POP3_HOST = "pop3.host"
POP3_PORT = "pop3.port"
POP3_LOGIN = "pop3.login"
POP3_PASSWORD = "pop3.password"

SMTP_STARTTLS = "smtp.starttls"
SMTP_HOST = "smtp.host"
SMTP_PORT = "smtp.port"
SMTP_LOGIN = "smtp.login"
SMTP_PASSWORD = "smtp.password"
SMTP_TO = "smtp.to"

# variable
params = dict()


def initialize(config_pathname):
    cfg = profig.Config(config_pathname)
    cfg.sync()
    params.update(cfg)


def get(key):
    return params[key]


def getInt(key):
    return int(params[key])


def _str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def getBool(key):
    return _str2bool(params[key])
