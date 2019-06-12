#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from tkinter import *
from tkinter.ttk import *
from core import Core
from tkinter import messagebox
from utils import System
from config import ConfigIO


class LicenseFrame(Frame):

    def __init__(self, root, stu_code, title='请输入（课君）使用许可 - 本软件免费', width=480, height=180):
        super().__init__()
        self.core = Core()
        self.root = root
        self.root.iconbitmap(System.resource_path("resource/icon.ico"))
        self.root.title(title)
        self.width = width
        self.height = height
        self.btn_submit = None
        self.text_machine_code = None
        self.auth_code = StringVar(value="")
        self.center_window()
        self.stu_code = stu_code
        self.create_form()
        self.root.mainloop()

    def create_form(self):
        self.root.minsize(self.width, self.height)
        self.root.maxsize(self.width, self.height)
        height_offset = 2
        object_interval = 20
        placeholder_width = 11
        init_padding = 15

        Label(self.root, text='机器码：', font=('微软雅黑', 10)).place(x=init_padding, y=20)
        Label(self.root, text='许可号：', font=('微软雅黑', 10)).place(x=init_padding, y=140)
        self.text_machine_code = Text(self.root)
        self.text_machine_code.insert(INSERT, self.core.machine_code(
            stu_code=self.stu_code,
        ))
        self.text_machine_code.place(x=init_padding + 5 * placeholder_width + object_interval, y=20 + height_offset, width=360, height=100)

        text_auth_code = Entry(self.root, textvariable=self.auth_code)
        text_auth_code.place(x=init_padding + 5 * placeholder_width + object_interval, y=140 + height_offset, width=250)
        self.btn_submit = Button(self.root, text='确定', command=self.set_license, width=11, state=NORMAL)
        self.btn_submit.place(x=init_padding + 5 * placeholder_width + object_interval + 285, y=140)

    @staticmethod
    def get_screen_size(window):
        return window.winfo_screenwidth(), window.winfo_screenheight()

    @staticmethod
    def get_window_size(window):
        return window.winfo_reqwidth(), window.winfo_reqheight()

    def center_window(self):
        _screen_width = self.root.winfo_screenwidth()
        _screen_height = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (
            self.width,
            self.height,
            (_screen_width - self.width) / 2,
            (_screen_height - self.height) / 2
        )
        self.root.geometry(size)

    def set_license(self):
        ConfigIO().auth(self.stu_code, self.auth_code.get().strip())
        f = messagebox.showinfo(title='成功', message='许可已设置，请重启软件，有问题请加群咨询：137991872')
        if f:
            sys.exit()


if __name__ == '__main__':
    page = LicenseFrame(Tk(), stu_code=None)

