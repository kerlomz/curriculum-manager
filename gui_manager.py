#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

from forms import login as login, main as main, init as init
from service import *


class GUIManager:
    def __init__(self, update_ui):
        self.update_ui = update_ui
        self.service = Service()
        self.frameDict = {}

    def get(self, _type):
        frame = self.frameDict.get(_type)

        if frame is None:
            frame = self.create(_type)
            self.frameDict[_type] = frame

        return frame

    def create(self, _type):
        if _type == 0:
            return init.InitFrame(parent=None, _type=_type, update_ui=self.update_ui, service=self.service)
        if _type == 1:
            return login.LoginFrame(parent=None, _type=_type, update_ui=self.update_ui, service=self.service)
        elif _type == 2:
            return main.MainFrame(parent=None, _type=_type, update_ui=self.update_ui, service=self.service)
