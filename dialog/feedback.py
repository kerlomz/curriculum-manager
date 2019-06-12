#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from wx import *
from wx.adv import *
from utils import *
from language.constants import *


class FeedbackDlg(Dialog):
    def __init__(self, parent=None, service=None):
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        Dialog.__init__(
            self,
            parent=parent,
            size=(420, 280)
        )
        self.Service = service
        self.Title = self.GUI.text(UI.Main.Dialog.Feedback.TITLE)
        self.info()

    def info(self):

        note_book = Notebook(
            self,
            -1,
            pos=(15, 20),
            size=(380, 170),
            style=NB_FIXEDWIDTH
        )
        feedback = TextCtrl(
            note_book,
            -1,
            style=TE_MULTILINE
        )
        tip_offs = TextCtrl(
            note_book,
            -1,
            style=TE_MULTILINE
        )
        note_book.AddPage(feedback, self.GUI.text(UI.Main.Dialog.Feedback.LABEL_FEEDBACK))
        note_book.AddPage(tip_offs, self.GUI.text(UI.Main.Dialog.Feedback.LABEL_TIP_OFFS))

        rect = self.GetClientRect()
        Button(
            self,
            id=ID_OK,
            label=self.GUI.text(UI.Main.Dialog.Default.BUTTON_CANCEL),
            pos=((rect[2] - 180) / 2, rect[3] - 35),
            size=(90, 25)
        )
        btn_submit = Button(
            self,
            id=NewId(),
            label=self.GUI.text(UI.Main.Dialog.Feedback.BUTTON_SUBMIT),
            pos=((rect[2] + 80) / 2, rect[3] - 35),
            size=(90, 25)
        )

        def submit():
            if feedback.Value == '' and tip_offs.Value == '':
                self.GUI.alert_message(
                    self.GUI.text(UI.Main.Dialog.Feedback.DLG_SUCCESS_TITLE),
                    self.GUI.text(Msg.Main.Feedback.NULL_SUBMIT)
                )
                return
            result = self.Service.feedback(feedback.Value, tip_offs.Value)
            if result:
                self.GUI.alert_message(
                    self.GUI.text(UI.Main.Dialog.Feedback.DLG_SUCCESS_TITLE),
                    self.GUI.text(Msg.Main.Feedback.SEND_SUCCESS)
                )
                self.Destroy()

        self.Bind(EVT_BUTTON, lambda x: submit(), btn_submit)


if __name__ == '__main__':
    app = App(False)
    aboutDlg = FeedbackDlg()
    aboutDlg.ShowModal()
