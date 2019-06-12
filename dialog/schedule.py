#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

from wx import *
from wx.html2 import *
from utils import *


class CurriculumSchedule(Dialog):
    def __init__(self, parent=None, service=None):
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        Dialog.__init__(
            self,
            parent=parent,
            size=(900, 700)
        )
        self.Title = self.GUI.text(UI.Main.Dialog.CourseTable.TITLE)
        self.service = service
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.browser = WebView.New(self)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.get_course()

    def get_course(self):
        if not self.service.login_validate():
            self.GUI.text([Msg.Login.LOGIN_CERTIFICATE_EXPIRED, Msg.Common.RETRYING])
            self.service.login_base()
            return self.get_course()
        else:
            html = self.service.get_course_table()
        self.browser.SetPage(html, "")


if __name__ == '__main__':
    app = App(False)
    course_dlg = CurriculumSchedule()
    course_dlg.ShowModal()
