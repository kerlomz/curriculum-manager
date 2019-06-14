#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

from wx import *
from gui_manager import *
from updater import Updater


class MainApp(App):

    def __init__(self):
        super(MainApp, self).__init__()

    def OnInit(self):
        self.manager = GUIManager(self.update_ui)
        if FIRST_TIME:
            self.frame = self.manager.get(0)
        else:
            self.frame = self.manager.get(1)
        self.frame.Show()
        return True

    def update_ui(self, _type):
        # self.frame.Show(False)
        self.frame.Destroy()
        self.frame = self.manager.get(_type)
        self.frame.Show(True)


def main():
    Updater.check_update()
    app = MainApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
