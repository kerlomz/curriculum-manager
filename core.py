#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import time
import hashlib
import base64
import socket
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from psutil import net_if_addrs
from config import Security

security = Security()
PUBLIC_KEY = security.public_key
PRIVATE_KEY = security.private_key
LOCAL_PUBLIC_KEY = security.local_public_key
LOCAL_PRIVATE_KEY = security.local_private_key


class RSAUtils(object):

    @staticmethod
    def encrypt(plain_text, local=False):
        public_key = RSA.importKey(LOCAL_PUBLIC_KEY if local else PUBLIC_KEY)
        _p = Cipher_pkcs1_v1_5.new(public_key)
        plain_text = plain_text.encode('utf-8') if isinstance(plain_text, str) else plain_text
        # 1024bit key
        try:
            default_encrypt_length = 117
            len_content = len(plain_text)
            if len_content < default_encrypt_length:
                return base64.b64encode(_p.encrypt(plain_text)).decode()
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_encrypt_length:
                    params_lst.append(_p.encrypt(plain_text[offset:offset + default_encrypt_length]))
                else:
                    params_lst.append(_p.encrypt(plain_text[offset:]))
                offset += default_encrypt_length
            target = b''.join(params_lst)
            return base64.b64encode(target).decode()
        except ValueError:
            return None

    @staticmethod
    def decrypt(cipher_text, decode=True, local=False):
        private_key = RSA.importKey(LOCAL_PRIVATE_KEY if local else PRIVATE_KEY)
        _pri = Cipher_pkcs1_v1_5.new(private_key)
        cipher_text = base64.b64decode(cipher_text if isinstance(cipher_text, bytes) else cipher_text.encode('utf-8'))
        # 1024bit key
        try:
            default_length = 128
            len_content = len(cipher_text)
            if len_content < default_length:
                return _pri.decrypt(cipher_text, "ERROR").decode()
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_length:
                    params_lst.append(_pri.decrypt(cipher_text[offset: offset + default_length], "ERROR"))
                else:
                    params_lst.append(_pri.decrypt(cipher_text[offset:], "ERROR"))
                offset += default_length
            target = b''.join(params_lst)
            return target.decode() if decode else target
        except ValueError:
            return None


class Core:

    @staticmethod
    def machine_code_auth(stu_code, c_volume_serial_number, mac_addr, hostname):
        auth_code = base64.b64encode(
            hashlib.md5("\u0000\u9999\0||{}||{}||{}||{}||\n\r\0\u8888".format(
                stu_code, c_volume_serial_number, mac_addr, hostname
            ).encode('utf8')).hexdigest().encode("utf8")
        ).decode()
        return auth_code[:6] + auth_code[-10:]

    @classmethod
    def mac_addr(cls):
        return [v[0][1] for v in net_if_addrs().values() if len(v[0][1]) == 17][0]

    @classmethod
    def hostname(cls):
        return socket.gethostname()

    @classmethod
    def c_volume_serial_number(cls):
        try:
            import win32api
            c_volume_serial_number = win32api.GetVolumeInformation("C:\\")[1]
            return str(c_volume_serial_number)
        except ImportError:
            return 0

    @classmethod
    def machine_code(cls, stu_code):
        c_volume_serial_number = cls.c_volume_serial_number
        mac = [v[0][1] for v in net_if_addrs().values() if len(v[0][1]) == 17][0]
        hostname = socket.gethostname()
        plain_text = "{}||{}||{}||{}||{}".format(stu_code, c_volume_serial_number, mac, hostname, time.time())
        encrypted = RSAUtils.encrypt(plain_text)
        encrypted = encrypted.replace("1", ")").replace("9", "{").replace("E", "&").replace("b", "%")
        encrypted = encrypted.replace(")", "9").replace("{", "1")
        return encrypted

    @classmethod
    def decrypt_auth(cls, key):
        key = key.replace("9", ")").replace("1", "{")
        key = key.replace(")", "1").replace("{", "9").replace("&", "E").replace("%", "b")
        plain_text = RSAUtils.decrypt(key)
        device_group = plain_text.split("||")
        stu_code = device_group[0]
        c_volume_serial_number = device_group[1]
        mac = device_group[2]
        hostname = device_group[3]
        auth_code = cls.machine_code_auth(stu_code, c_volume_serial_number, mac, hostname)
        return auth_code


if __name__ == '__main__':
    r = Core.decrypt_auth(
        "O/zxgDfnn3+4&5/y5sK3t%aah4C6nM2zx9x40/JcM%tzUW50H0PpdQ%4W3/kA9N/VneyLs8rSD719s2e1/p4C/epVXdWONnK0lR4gPaHFVJka5qzDynfuwGdtAcP0S&Xi7hyuHjcDh0zi58Ui1CuUIZvq4dkLnsMwCrrS2zRzXQ=")
    print(r)
