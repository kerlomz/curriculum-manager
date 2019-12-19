#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os
import logging
import locale
import pickle
import yaml
from constants import *

FIRST_TIME = False

DEFAULT_CONF = {
    "Service": {
        "Host": "xk.zucc.edu.cn",
        "Auth": "47.96.22.125",
    },
    "Cache": {
        "Courses": "",
        "CSRF": ""
    },
    "Certificate": {
        "Account": "",
        "Session": "",
        "DynamicCode": ""
    },
    "System": {
        "Language": locale.getdefaultlocale()[0],
        "Remember": True
    },
    "License": {}
}

logging.basicConfig(filename='client.log',
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.INFO)

CONFIG_PATH = StaticPath.System.CONFIG_PATH


class ConfigIO:

    @staticmethod
    def read():
        with open(CONFIG_PATH, 'r', encoding="utf-8") as conf_fp:
            stream = conf_fp.read()
            return yaml.load(stream, Loader=yaml.SafeLoader)

    @staticmethod
    def dump(value=None):
        if not value:
            value = cf
        with open(CONFIG_PATH, 'w', encoding="utf-8") as conf_fp:
            yaml.dump(
                value,
                conf_fp,
                default_flow_style=False,
                line_break=False,
                canonical=True,
                indent=10
            )

    @staticmethod
    def update(root: str, node: str, value):
        cf[root][node] = value
        ConfigIO.dump()

    @staticmethod
    def auth(stu_code, auth_code):
        cf['License'].update({stu_code: auth_code})
        ConfigIO.dump()


if not os.path.exists(CONFIG_PATH):
    ConfigIO.dump(DEFAULT_CONF)

cf = ConfigIO.read()

CACHE = cf.get('Cache')
SERVICE = cf.get("Service")
SYSTEM = cf.get('System')
LICENSE = cf.get('License')
SAVED_ACCOUNT = cf['Certificate']
LOGIN_INFO = SAVED_ACCOUNT['Account']
LAST_CSRF = CACHE['CSRF']
SESSION = SAVED_ACCOUNT['Session']
DYNAMIC_CODE = SAVED_ACCOUNT['DynamicCode']
NEED_AGREEMENT = True


class Cache(object):

    @staticmethod
    def save(obj):
        return pickle.dumps(obj) if obj else obj

    @staticmethod
    def open(obj):
        return pickle.loads(obj) if obj else obj


class NetworkConfig:
    HOST_SERVER = SERVICE.get('Host')
    AUTH_SERVER = DEFAULT_CONF['Service']['Auth']
    CAPTCHA_API = DEFAULT_CONF['Service']['Auth']


class SystemConfig:
    HEARTBEAT_INTERVAL = 10
    CHECK_SERVER_ON_START = False
    LANGUAGE = SYSTEM.get('Language')
    CLIENT_VER = '1.0.6'
    EMAIL = 'kerlomz@gmail.com'
    AUTHOR = 'Mr.Zhou'


class UserConfig(object):
    REMEMBER = SYSTEM.get('Remember')
    COURSE_DATA = CACHE.get('Courses')


class Curricula:
    MAX_SELECTED_CURRICULA = 1
