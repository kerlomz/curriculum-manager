#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import qrcode
from wx import *
from utils import *
from language.constants import *


class DonateDlg(Dialog):
    def __init__(self, parent=None):
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        Dialog.__init__(
            self,
            parent=parent,
            size=(360, 300)
        )
        self.Title = self.GUI.text(UI.Main.Dialog.Donate.TITLE)
        self.donate_img()
        self.info()

    def donate_img(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=0,
        )
        qr.add_data('https://qr.alipay.com/fkx09880nqh97rfj4hijv52')
        qr.make(fit=True)

        pil_img = qr.make_image()
        image = Image(pil_img.size[0], pil_img.size[1])
        image.SetData(pil_img.convert("RGB").tobytes())
        width = image.GetWidth()
        StaticBitmap(
            self,
            -1,
            Bitmap(image),
            pos=((360 - width) / 2 - 5, 20)
        )

    def info(self):

        StaticText(
            self,
            label=self.GUI.text(UI.Main.Dialog.Donate.LABEL_DONATE),
            pos=(15, 180)
        )

        rect = self.GetClientRect()
        Button(
            self,
            id=ID_OK,
            label=self.GUI.text(UI.Main.Dialog.Default.BUTTON_CONFIRM),
            pos=((rect[2] - 60) / 2, rect[3] - 35),
            size=(80, 25)
        )


if __name__ == '__main__':
    app = App(False)
    aboutDlg = DonateDlg()
    aboutDlg.ShowModal()
