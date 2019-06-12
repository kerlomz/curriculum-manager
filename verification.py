#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from core import Core
from entity import ClientMessage, Device, MessageType
from config import NetworkConfig, LICENSE
from utils import ResponseParser


class GoogleRPC(object):

    def __init__(self):

        self.core = Core()

    def verify(self, stu_code):
        device = Device().from_core(self.core)
        for k, v in LICENSE.items():
            device.add_license(k, v)
        response = ResponseParser(NetworkConfig.AUTH_SERVER, port=5449).request(
            ClientMessage(
                device=device,
                stu_code=stu_code
            ).send(
                body={"question": "are you ready?"},
                context_type=MessageType.Verify,
            )
        )
        resp_context = response.context.body
        if not resp_context or not resp_context.get('success'):
            print('网络验证未通过')
            return False
        else:
            print('网络验证通过')
            return True
