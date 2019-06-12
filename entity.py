#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import time
import hashlib
from enum import Enum, unique


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

    def from_core(self, core):
        self.new(
            mac_addr=core.mac_addr,
            hostname=core.hostname,
            c_volume_serial_number=core.c_volume_serial_number
        )
        return self

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
        self.__auth_license__.update({stu_code: auth_license})
        return self


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
        self.__ver__: str = ver if ver else 1.0

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

    @property
    def now(self):
        return time.time()

    @property
    def context(self):
        from core import Core
        auth_code = self.device.auth_license.get(self.student_code)
        calc_auth_code = Core.machine_code_auth(
            stu_code=self.student_code,
            c_volume_serial_number=self.device.c_volume_serial_number,
            mac_addr=self.device.mac_addr,
            hostname=self.device.hostname)

        if self.__timestamp__ > self.now + 300 or self.__timestamp__ < self.now - 300:
            return Context(message="Forged timestamp suspected!", code=-997, context_type=MessageType.Error)
        if auth_code != calc_auth_code:
            return Context(message="Illegal authorization!", code=-998, context_type=MessageType.Error)
        if self.__sign__ != self.sign:
            return Context(message="Forged sign suspected!", code=-999, context_type=MessageType.Alert)
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
