#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from wx import *
from utils import *


class InitFrame(Frame):
    """ Login Form """

    def __init__(self, parent=None, _type=-1, update_ui=None, service=None):

        Frame.__init__(self, parent)
        self.Size = (480, 150)
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        self.UpdateUI = update_ui
        self.Centre()
        self.method_map = {
            self.GUI.text(Msg.Common.NORTH_CAMPUS): 1,
            self.GUI.text(Msg.Common.SOUTH_CAMPUS): 2,
            self.GUI.text(Msg.Common.ROUTE_METHOD): 3,
            self.GUI.text(Msg.Common.LAB_LIBRARY): 4
        }
        self.AppLogo = Icon(System.resource_path(StaticPath.System.APP_ICON_PATH), BITMAP_TYPE_ICO)
        self.SetIcon(self.AppLogo)
        self.init()

    def set_config(self, e):
        label = e.GetEventObject().GetLabel()
        if self.method_map[label] == 1:
            set_config('server', 'host', 'xk.zucc.edu.cn')
            NetworkConfig.HOST_SERVER = 'xk.zucc.edu.cn'
        elif self.method_map[label] == 2:
            import win32api
            set_config('server', 'host', '10.61.5.17')
            NetworkConfig.HOST_SERVER = '10.61.5.17'
            path = File.resource_path('nat.exe')
            win32api.ShellExecute(0, 'open', path, '', '', 0)
        elif self.method_map[label] == 3:
            set_config('server', 'host', 'xk.zucc.edu.cn')
            NetworkConfig.HOST_SERVER = 'xk.zucc.edu.cn'
        elif self.method_map[label] == 4:
            set_config('server', 'host', '10.61.5.17')
            NetworkConfig.HOST_SERVER = '10.61.5.17'

    def init(self):
        """ Init Form """
        self.Title = self.GUI.text(UI.Login.TITLE, SystemConfig.CLIENT_VER)
        panel = Panel(self, NewId())

        rect = self.GetClientRect()

        radio_north = RadioButton(panel, -1, self.GUI.text(Msg.Common.NORTH_CAMPUS), pos=(rect[0] + 20, rect[1] - 3 + 35))
        self.Bind(EVT_RADIOBUTTON, self.set_config, radio_north)
        radio_south = RadioButton(panel, -1, self.GUI.text(Msg.Common.SOUTH_CAMPUS), pos=(rect[0] + 120, rect[1] - 3 + 35))
        self.Bind(EVT_RADIOBUTTON, self.set_config, radio_south)
        radio_route = RadioButton(panel, -1, self.GUI.text(Msg.Common.ROUTE_METHOD), pos=(rect[0] + 220, rect[1] - 3 + 35))
        self.Bind(EVT_RADIOBUTTON, self.set_config, radio_route)
        radio_lab = RadioButton(panel, -1, self.GUI.text(Msg.Common.LAB_LIBRARY), pos=(rect[0] + 320, rect[1] - 3 + 35))
        self.Bind(EVT_RADIOBUTTON, self.set_config, radio_lab)

        def submit(e):
            self.UpdateUI(1)

        button_submit = Button(
            panel,
            label=self.GUI.text(UI.Main.Dialog.Default.BUTTON_CONFIRM),
            size=(90, 25),
            pos=(rect[0] + 320, rect[1] + 65)
        )
        self.Bind(EVT_BUTTON, submit, button_submit)