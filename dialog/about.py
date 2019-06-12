#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from wx import *
from wx.adv import *
from utils import *
from language.constants import *


class AboutDlg(Dialog):
    def __init__(self, parent=None):
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        Dialog.__init__(
            self,
            parent=parent,
            size=(420, 560)
        )
        self.Title = self.GUI.text(UI.Main.Dialog.About.TITLE)
        self.author_img()
        self.info()
        # self.Center()

    # -----创建控件-----
    def author_img(self):
        img = Image(System.resource_path(StaticPath.System.AUTHOR_IMG_PATH), BITMAP_TYPE_ANY)
        width = img.GetWidth()
        StaticBitmap(
            self,
            -1,
            Bitmap(img),
            pos=((400 - width) / 2 - 5, 20)
        )

    # --软件信息
    def info(self):
        group_box = StaticBox(
            self,
            label=self.GUI.text(UI.Main.Dialog.About.INFO_TITLE),
            pos=(15, 180),
            size=(365+10, 120)
        )
        rect = group_box.Rect
        lbl_version = StaticText(
            self,
            label=self.GUI.text(UI.Main.Dialog.About.LABEL_VERSION, SystemConfig.CLIENT_VER),
            pos=(rect[0] + 20, rect[1] + 30)
        )
        rect = lbl_version.Rect
        lbl_author = StaticText(
            self,
            label=self.GUI.text(UI.Main.Dialog.About.LABEL_AUTHOR, SystemConfig.AUTHOR),
            pos=(rect[0], rect[1] + 25)
        )
        rect = lbl_author.Rect
        lbl_wid_email = StaticText(
            self,
            label=self.GUI.text(UI.Main.Dialog.About.LABEL_EMAIL),
            pos=(rect[0], rect[1] + 25)
        )
        rect = lbl_wid_email.Rect
        HyperlinkCtrl(
            self,
            id=-1,
            label=SystemConfig.EMAIL,
            url='mailto:{}'.format(SystemConfig.EMAIL),
            pos=(rect[0] + rect[2] + 10, rect[1])
        )

        # --选项卡
        rect = group_box.Rect
        note_book = Notebook(
            self,
            -1,
            pos=(rect[0], rect[1] + rect[3] + 10),
            size=(rect[2] + 10, 170),
            style=NB_FIXEDWIDTH
        )
        txt_introduction = TextCtrl(
            note_book,
            -1,
            style=ALL | TE_READONLY
        )
        txt_license = TextCtrl(
            note_book,
            -1,
            style=ALL | TE_READONLY
        )
        txt_others = TextCtrl(
            note_book,
            -1,
            style=ALL | TE_READONLY
        )
        note_book.AddPage(txt_introduction, self.GUI.text(UI.Main.Dialog.About.LABEL_INTRODUCTION))
        note_book.AddPage(txt_license, self.GUI.text(UI.Main.Dialog.About.LABEL_LICENSE))
        note_book.AddPage(txt_others, self.GUI.text(UI.Main.Dialog.About.LABEL_OTHERS))

        # 设置介绍、协议、其他文本框中的内容
        txt_introduction.SetValue(self.GUI.text(Msg.Main.About.INTRODUCTION))
        txt_license.SetValue(self.GUI.text(Msg.Main.About.LICENSE))
        txt_others.SetValue(self.GUI.text(Msg.Main.About.OTHERS))

        rect = self.GetClientRect()
        Button(
            self,
            id=ID_OK,
            label=self.GUI.text(UI.Main.Dialog.Default.BUTTON_CONFIRM),
            pos=((rect[2] - 60) / 2, rect[3] - 35),
            size=(90, 25)
        )


if __name__ == '__main__':
    app = App(False)
    aboutDlg = AboutDlg()
    aboutDlg.ShowModal()
