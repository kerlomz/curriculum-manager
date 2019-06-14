#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import time
import json
import hashlib
from enum import Enum, unique
from core import Core, RSAUtils


@unique
class MessageType(Enum):
    Error = 'Error'
    Report = 'Report'
    Logging = 'Log'
    Alert = 'Alert'
    Control = 'Control'
    Config = 'Config'
    Heartbeat = 'Heartbeat'
    Verify = 'Verify'
    Info = 'Info'
    Undefined = 'Undefined'
    Warning = 'Warning'


class Device(object):

    def __init__(self, mac_addr=None, hostname=None, c_volume_serial_number=None, auth_license=None):
        self.__mac_addr__: str = mac_addr if mac_addr else None
        self.__hostname__: str = hostname if hostname else None
        self.__c_volume_serial_number__: str = c_volume_serial_number if c_volume_serial_number else None
        self.__auth_license__: dict = auth_license if auth_license else {}

    def __repr__(self):
        return "Device's mac_addr is : {}, hostname is {}, c_volume_serial_number is {}, auth_license is {}".format(
            self.mac_addr, self.hostname, self.c_volume_serial_number, self.auth_license
        )

    def dumps(self, with_license=True, with_id=False):
        device = {
            "mac_addr": self.mac_addr,
            "hostname": self.hostname,
            "c_volume_serial_number": self.c_volume_serial_number
        }
        if with_license:
            device["auth_license"] = self.auth_license
        if with_id:
            device["id"] = hashlib.md5(device).hexdigest()
        return json.dumps(device, ensure_ascii=False, separators=(',', ':'), sort_keys=True)

    def from_core(self):
        self.new(
            mac_addr=Core.mac_addr(),
            hostname=Core.hostname(),
            c_volume_serial_number=Core.c_volume_serial_number(),
        )
        return self

    @property
    def device_id(self):
        return hashlib.md5(self.dumps(with_license=False, with_id=False)).hexdigest()

    @property
    def mac_addr(self):
        return self.__mac_addr__

    @property
    def hostname(self):
        return self.__hostname__

    @property
    def c_volume_serial_number(self):
        return self.__c_volume_serial_number__

    @property
    def auth_license(self):
        return self.__auth_license__

    def new(self, mac_addr, hostname, c_volume_serial_number, auth_license=None):
        self.__mac_addr__ = mac_addr
        self.__hostname__ = hostname
        self.__c_volume_serial_number__ = c_volume_serial_number
        self.__auth_license__ = auth_license if auth_license else self.__auth_license__

    def add_license(self, stu_code: str, auth_license: str):
        if not stu_code:
            return self
        self.__auth_license__[stu_code] = auth_license
        return self

    @classmethod
    def decrypt_auth2object(cls, machine_code):
        key = machine_code.replace("9", ")").replace("1", "{")
        key = key.replace(")", "1").replace("{", "9").replace("&", "E").replace("%", "b")
        plain_text = RSAUtils.decrypt(key)
        device_group = plain_text.split("||")
        stu_code = device_group[0]
        c_volume_serial_number = device_group[1]
        mac_addr = device_group[2]
        hostname = device_group[3]
        device = Device(mac_addr=mac_addr, hostname=hostname, c_volume_serial_number=c_volume_serial_number)
        machine_code_auth = Core.machine_code_auth(stu_code, c_volume_serial_number, mac_addr, hostname)
        device.add_license(stu_code, machine_code_auth)
        return device


class Context(object):

    def __init__(self, body: dict = None, message: str = None, code: int = None, context_type: MessageType = None):
        self.body = body if body else {}
        self.message = message if message else ""
        self.code = code if code else 0x000
        self.context_type: MessageType = context_type if context_type else MessageType.Undefined

    def __repr__(self):
        return self.message


class ServerMessage(object):

    def __init__(self, ver: float = None):
        self.__suffix___: str = '/|/!/!/@Z#H$O%U^---|'
        self.__context__: Context = Context()
        self.__timestamp__: float = 0.
        self.__sign__: str = None
        self.__ver__: float = ver if ver else 1.0

    @property
    def now(self):
        return time.time()

    @property
    def version(self):
        return str(self.__ver__)

    @property
    def timestamp(self):
        return str(self.__timestamp__)

    @property
    def sign(self):
        return hashlib.md5("&&".join(
            [
                '&'.join(['{}={}'.format(k, v) for (k, v) in sorted(self.__context__.body.items())]),
                self.timestamp,
                self.version,
                self.__context__.message,
                self.__suffix___,
            ]
        ).encode()).hexdigest()

    @property
    def context(self):
        if self.__timestamp__ > self.now + 300 or self.__timestamp__ < self.now - 300:
            return Context(message="Forged timestamp suspected!", code=-999, context_type=MessageType.Error)
        if self.__sign__ != self.sign:
            return Context(message="Forged message suspected!", code=-998, context_type=MessageType.Alert)
        return self.__context__

    def set_message(self, message: Context):
        self.__context__ = message
        self.__timestamp__ = time.time()
        self.__sign__ = self.sign

    def send(self, body: dict = None, code: int = None, context_type: MessageType = None, context: Context = None):
        if context:
            self.set_message(context)
        else:
            self.set_message(Context(body=body, code=code, context_type=context_type))
        return self


class ClientMessage(object):

    def __init__(self, device: Device = None, stu_code: str = None):
        self.__suffix___: str = '/|/!/!/@Z#H$O%U^---|'
        self.__context__: Context = Context()
        self.__timestamp__: float = 0.
        self.__sign__: str = None
        self.__device__: Device = device if device else None
        self.__student_code__: str = stu_code if stu_code else None
        self.__auth_license__: str = self.device.auth_license.get(self.student_code)

    @property
    def now(self):
        return time.time()

    @property
    def context(self):
        calc_auth_code = Core.machine_code_auth(
            stu_code=self.student_code,
            c_volume_serial_number=self.device.c_volume_serial_number,
            mac_addr=self.device.mac_addr,
            hostname=self.device.hostname)

        if self.__timestamp__ > self.now + 300 or self.__timestamp__ < self.now - 300:
            return Context(
                body=self.__context__.body,
                message="Forged timestamp suspected!",
                code=-997,
                context_type=MessageType.Error
            )
        if self.__auth_license__ != calc_auth_code:
            return Context(
                body=self.__context__.body,
                message="Illegal authorization!",
                code=-998,
                context_type=MessageType.Error
            )
        if self.__sign__ != self.sign:
            return Context(
                body=self.__context__.body,
                message="Forged sign suspected!",
                code=-999,
                context_type=MessageType.Alert
            )
        return self.__context__

    @property
    def timestamp(self):
        return str(self.__timestamp__)

    @property
    def device(self):
        return self.__device__

    @property
    def student_code(self):
        return self.__student_code__

    @property
    def auth_license(self):
        return self.__auth_license__

    @property
    def sign(self):
        return hashlib.md5("&&".join(
            [
                '&'.join(['{}={}'.format(k, v) for (k, v) in sorted(self.__context__.body.items())]),
                self.timestamp,
                self.student_code,
                self.__context__.message,
                self.__suffix___,
            ]
        ).encode()).hexdigest()

    def set_message(self, message: Context):
        if not self.device:
            raise ValueError("Message entity has not been initialized!")
        self.__context__ = message
        self.__timestamp__ = time.time()
        self.__sign__ = self.sign

    def send(self, body: dict = None, code: int = None, context_type: MessageType = None, context: Context = None):
        if context:
            self.set_message(context)
        else:
            self.set_message(Context(body=body, code=code, context_type=context_type))
        return self

    def init(self, device: Device = None, student_code: str = None):
        self.__device__ = device if device else self.__device__
        self.__student_code__ = student_code if student_code else self.__student_code__
