#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import tkinter
from wx import *
from utils import *
from service import *
import menu as m
from auth_dialog import LicenseFrame
from core import Core
from google_rpc import GoogleRPC


class LoginFrame(Frame):
    """ Login Form """

    def __init__(self, parent=None, _type=-1, update_ui=None, service=None):

        Frame.__init__(self, parent)
        # self.core = Core()
        self.Size = (340, 200)
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        self.UpdateUI = update_ui
        self.Centre()
        self.AppLogo = Icon(System.resource_path(StaticPath.System.APP_ICON_PATH), BITMAP_TYPE_ICO)
        self.SetIcon(self.AppLogo)
        self.status_bar = self.CreateStatusBar()
        self.Service = service
        self.Service.init(self, self.GUI, self.status_bar)
        self.default_certificate = ['', '']
        self.init_conf()
        self.init()

    def init_conf(self):
        decrypted_login_info = RSAUtils.decrypt(LOGIN_INFO, decode=False, local=True)
        default_certificate = Cache.open(decrypted_login_info) if decrypted_login_info else ['', '']
        dynamic_code = Cache.open(RSAUtils.decrypt(DYNAMIC_CODE, decode=False, local=True))
        last_csrf = Cache.open(RSAUtils.decrypt(LAST_CSRF, decode=False, local=True))
        self.default_certificate = default_certificate if default_certificate else self.default_certificate
        self.Service.set_login(self.default_certificate[0], self.default_certificate[1], dynamic_code)
        self.Service.csrf_token = last_csrf if last_csrf else {
            "Login": '',
            "GeneralElectiveCourseList": '',
            "GeneralElectiveCoursePost": '',
            "CompulsoryCoursePage": '',
            "CompulsoryCourseList": '',
            "CompulsoryCoursePost": '',
        }

    def init(self):
        """ Init Form """
        self.Title = self.GUI.text(UI.Login.TITLE, SystemConfig.CLIENT_VER)
        panel = Panel(self, NewId())

        rect = self.GetClientRect()

        label_text = [self.GUI.text(UI.Login.LABEL_ID), self.GUI.text(UI.Login.LABEL_PWD)]

        label_widget = [StaticText(
            panel,
            label=text,
            pos=(rect[0] + 15, rect[1] + 15 + i * 35),
        ) for i, text, in enumerate(label_text)]

        rect = label_widget[0].Rect
        entry_style = [TE_LEFT | TE_PROCESS_ENTER, TE_PASSWORD | TE_PROCESS_ENTER]
        entry_widget = [TextCtrl(
            panel,
            size=(190, -1),
            pos=(rect[0] + 70, rect[1] - 3 + i * 35),
            style=style
        ) for i, style, in enumerate(entry_style)]

        student_code, password = entry_widget[0], entry_widget[1]

        student_code.SetValue(self.default_certificate[0])
        password.SetValue(self.default_certificate[1])

        if student_code.GetValue():
            password.SetFocus()

        rect = entry_widget[1].Rect
        button_submit = Button(
            panel,
            label=self.GUI.text(UI.Login.BUTTON_SUBMIT),
            size=(90, 25),
            pos=(rect[0] + 100, rect[1] + 35)
        )

        check_remember = CheckBox(
            panel,
            NewId(),
            label=self.GUI.text(UI.Login.CHECK_BOX_REMEMBER),
            pos=(rect[0] - 70, rect[1] + 40)
        )
        check_remember.SetValue(UserConfig.REMEMBER)

        check_remember.Bind(
            EVT_CHECKBOX,
            lambda x: ConfigIO.update('System', 'Remember', check_remember.Value),
            check_remember
        )

        def submit(e):
            uid = entry_widget[0].GetValue()
            pwd = entry_widget[1].GetValue()
            self.Service.set_login(uid, pwd)
            stu_code = self.Service.student_code
            print(stu_code)
            auth_code = Core.machine_code_auth(
                stu_code=stu_code,
                c_volume_serial_number=Core.c_volume_serial_number(),
                mac_addr=Core.mac_addr(),
                hostname=Core.hostname()
            )
            if check_remember.IsChecked():
                ConfigIO.update(
                    "Certificate",
                    "Account",
                    value=RSAUtils.encrypt(Cache.save([uid, pwd]), local=True)
                )
            if auth_code != LICENSE.get(stu_code):
                print("1111", LICENSE, auth_code)
                LicenseFrame(tkinter.Tk(), stu_code=stu_code)
                GUI.alert_error(
                    self.GUI.text(UI.Main.Dialog.Error.TITLE),
                    self.GUI.text(Msg.Main.LICENSE_ERROR)
                )
                exit(-999)

            resp_context = GoogleRPC.verify(stu_code=stu_code)
            if not resp_context or not resp_context.get('success'):
                GUI.alert_error(
                    self.GUI.text(UI.Main.Dialog.Error.TITLE),
                    self.GUI.text(Msg.Main.LICENSE_ERROR)
                )
                exit(-1)
            raw_cookie = Cache.open(RSAUtils.decrypt(SESSION, decode=False, local=True))

            logged_in = self.Service.login_validate(raw_cookie=raw_cookie)
            if logged_in:
                print('状态: Cookie 有效')
                self.Service.agreement_status = True
                resp = {"message": None, "status": True}
            else:
                resp = self.Service.login_base()

            # TODO 上报切换账号
            if self.default_certificate[0] != '' and uid != self.default_certificate[0]:
                print('切换账号预警')

            if not UserConfig.COURSE_DATA:
                self.Service.agreement()

            if resp['status']:
                # TODO 网络验证，是否有许可

                if check_remember.IsChecked():
                    ConfigIO.update(
                        "Certificate",
                        "Account",
                        value=RSAUtils.encrypt(Cache.save([uid, pwd]), local=True)
                    )
                else:
                    pass
                self.UpdateUI(2)
            else:
                self.status_bar.SetStatusText(
                    self.GUI.text(Msg.Login.LOGIN_FAILED, resp['message'])
                )
                return

        self.Bind(EVT_BUTTON, submit, button_submit)
        self.Bind(EVT_TEXT_ENTER, submit, password)
        self.GUI.build_menu(self, m.MenuWidget(self, self.Service).menu_data(False))
