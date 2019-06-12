#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import base64
import grpc
import grpc_pb2
import grpc_pb2_grpc
from config import NetworkConfig
from utils import System


class Interface(object):

    @staticmethod
    def remote_predict(img_bytes):
        if not System.test_image(img_bytes):
            return None
        channel = grpc.insecure_channel('{}:5449'.format(NetworkConfig.CAPTCHA_API))
        stub = grpc_pb2_grpc.PredictStub(channel)
        response = stub.predict(grpc_pb2.PredictRequest(
            image=base64.b64encode(img_bytes).decode(), split_char=',', model_type=None, model_site=None
        ))
        return response.result

