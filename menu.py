#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import platform
import threading
import webbrowser
from dialog import *


class MenuWidget(object):
    def __init__(self, parent, service):
        self.parent = parent
        self.Service = service
        self.GUI = GUI(parent, SystemConfig.LANGUAGE)
        self.handler = MenuHandler(parent, self.Service)

    def menu_data(self, is_login):
        """
        Menu Data
        :return:
        """
        return [
            (self.GUI.text(UI.Main.Menu.Opr.OPERATION), [
                (self.GUI.text(UI.Main.Menu.Opr.STOP_WORK), "", self.handler.on_kill_thread),
                (self.GUI.text(UI.Main.Menu.Opr.NAT_ROUTE), "", self.handler.on_nat_route),
                ("", "", ""),
                (self.GUI.text(UI.Main.Menu.Opr.LOGOUT), "", self.handler.on_logout),
                (self.GUI.text(UI.Main.Menu.Opr.QUIT), "", self.handler.on_exit)]),
            (self.GUI.text(UI.Main.Menu.Mine.MINE), [
                (self.GUI.text(UI.Main.Menu.Mine.COURSE_TABLE), "", self.handler.on_schedule),
                (self.GUI.text(UI.Main.Menu.Mine.DONATE), "", self.handler.on_donate)]),
            (self.GUI.text(UI.Main.Menu.Help.HELP), [
                (self.GUI.text(UI.Main.Menu.Help.ABOUT), "", self.handler.on_about),
            ]),

        ] if is_login else [
            (self.GUI.text(UI.Main.Menu.Opr.OPERATION), [
                (self.GUI.text(UI.Main.Menu.Opr.NAT_ROUTE), "", self.handler.on_nat_route),
                (self.GUI.text(UI.Main.Menu.Opr.QUIT), "", self.handler.on_exit)]),
            (self.GUI.text(UI.Main.Menu.Help.HELP), [
                (self.GUI.text(UI.Main.Menu.Help.ABOUT), "", self.handler.on_about)])
        ]


class MenuHandler(object):
    def __init__(self, parent, service):
        self.parent = parent
        self.Service = service
        self.GUI = GUI(parent, SystemConfig.LANGUAGE)

    def on_schedule(self, e):
        dlg = CurriculumSchedule(self.parent, service=self.Service)
        dlg.ShowModal()
        dlg.Destroy()

    @staticmethod
    def on_nat_route(e):
        if 'Windows' in platform.system():
            import win32api
            path = File.resource_path('nat.exe')
            win32api.ShellExecute(0, 'open', path, '', '', 0)
            webbrowser.open('http://10.61.2.6', new=0, autoraise=True)
        elif 'Linux' in platform.system():
            pass
        elif 'Darwin' in platform.system():
            pass

    @staticmethod
    def on_donate(e):
        dlg = DonateDlg()
        dlg.ShowModal()
        dlg.Destroy()

    def on_feedback(self, e):
        dlg = FeedbackDlg(service=self.Service)
        dlg.ShowModal()
        dlg.Destroy()

    @staticmethod
    def on_about(e):
        dlg = AboutDlg()
        dlg.ShowModal()
        dlg.Destroy()

    def on_kill_thread(self, e):
        self.Service.kill_thread()

    def on_check_update(self, e):
        self.Service.check_update()

    def on_logout(self, e):
        th = threading.Thread(target=self.Service.logout)
        th.setDaemon(True)
        th.start()

    def on_exit(self, e):
        """
        Menu Event On Exit
        :param e:
        """
        self.parent.Close(True)
