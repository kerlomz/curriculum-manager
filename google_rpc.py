#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from core import Core
from entity import ClientMessage, Device, MessageType
from config import NetworkConfig, LICENSE
from utils import ResponseParser


class GoogleRPC(object):

    @classmethod
    def base(cls, context_type, stu_code, body):
        device = Device().from_core()
        for k, v in LICENSE.items():
            device.add_license(k, v)
        response = ResponseParser(NetworkConfig.AUTH_SERVER, port=5449).request(
            ClientMessage(
                device=device,
                stu_code=stu_code
            ).send(
                body=body,
                context_type=context_type,
            )
        )
        resp_context = response.context.body
        return resp_context

    @classmethod
    def verify(cls, stu_code):
        return cls.base(MessageType.Verify, stu_code, {"question": "are you ready?"})

    @classmethod
    def heartbeat(cls, stu_code, course):
        cls.base(MessageType.Heartbeat, stu_code, {"course": course})

    @classmethod
    def control(cls, stu_code, course):
        return cls.base(MessageType.Control, stu_code, {"course": course})
