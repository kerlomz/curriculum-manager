#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import threading
from wx import *
from widget.check_list_ctrl import CheckListCtrl
from service import *
import menu as m
from dialog.compulsory import CompulsoryDlg


class MainFrame(Frame):
    """ Main Form """
    def __init__(self, parent=None, _type=-1, update_ui=None, service=None):
        Frame.__init__(self, parent)
        self.Size = (640, 730)
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        self.UpdateUI = update_ui
        self.Centre()
        self.AppLogo = Icon(System.resource_path(StaticPath.System.APP_ICON_PATH), BITMAP_TYPE_ICO)
        self.SetIcon(self.AppLogo)
        self.status_bar = self.CreateStatusBar()
        self.RemainLabel = None
        self.Service = service
        self.course_data = []
        self.Service.init(self, self.GUI, self.status_bar)
        self.init()

    def init(self):
        """ Init Form """
        self.Title = self.GUI.text(UI.Main.TITLE, self.Service.fullname)
        panel = Panel(self, NewId())

        rect = self.GetClientRect()

        """ Search Bar """
        group_search = StaticBox(
            panel,
            label=self.GUI.text(UI.Main.PANEL_TITLE_SEARCH),
            pos=(rect[0] + 10, rect[1] + 10),
            size=(430, 60)
        )
        rect = group_search.Rect
        entry_search = TextCtrl(
            panel,
            size=(rect[2] - 110, -1),
            pos=(rect[0] + 10, rect[1] + 20),
            style=TE_LEFT | TE_PROCESS_ENTER,
        )
        entry_search.SetMaxLength(10)
        button_search = Button(
            panel,
            label=self.GUI.text(UI.Main.BUTTON_SEARCH),
            size=(80, 25),
            pos=(rect[2] - 80, 30)
        )
        rect = button_search.Rect
        btn_compulsory = Button(
            panel,
            label=self.GUI.text(UI.Main.BUTTON_COMPULSORY),
            size=(150, 25),
            pos=(rect[0] + 100, 30)
        )
        btn_compulsory.Disable()

        """ Course List """
        rect = group_search.Rect
        group_course = StaticBox(
            panel,
            label=self.GUI.text(UI.Main.PANEL_TITLE_COURSE),
            pos=(rect[0], rect[1] + rect[3] + 20),
            size=(600, 180)
        )
        rect = group_course.Rect
        lst_course = CheckListCtrl(
            panel,
            pos=(rect[0] + 10, rect[1] + 20),
            style=LC_REPORT | LC_HRULES | LC_VRULES,
            size=(rect[2] - 20, rect[3] - 30)
        )
        w = lst_course.Rect[2]
        for i, ratio in enumerate([0.06, 0.35, 0.3, 0.15, 0.1, 0, 0, 0, 0, 0]):
            lst_course.InsertColumn(
                col=i+1,
                heading=self.GUI.text(UI.Main().__getattribute__('COURSE_LIST_COL_{}'.format(i+1))),
                width=w * ratio
            )

        self.Service.ctrl_ref['ExpectedCourseList'] = lst_course
        """ Logger List """
        rect = group_course.Rect
        group_logger = StaticBox(
            panel,
            label=self.GUI.text(UI.Main.PANEL_TITLE_LOGGER),
            pos=(rect[0], rect[1] + rect[3] + 20),
            size=(600, 160)
        )
        rect = group_logger.Rect
        lst_logger = ListCtrl(
            panel,
            pos=(rect[0] + 10, rect[1] + 20),
            style=LC_REPORT | LC_HRULES | LC_VRULES,
            size=(rect[2] - 20, rect[3] - 30)
        )
        w = lst_logger.Rect[2]
        lst_logger.InsertColumn(col=0, heading=self.GUI.text(UI.Main.LOG_LIST_COL_1), width=w * 0.08)
        lst_logger.InsertColumn(col=1, heading=self.GUI.text(UI.Main.LOG_LIST_COL_2), width=w * 0.38)
        lst_logger.InsertColumn(col=2, heading=self.GUI.text(UI.Main.LOG_LIST_COL_3), width=w * 0.5)

        self.Service.ctrl_ref['LoggerList'] = lst_logger

        """ Selected List """
        rect = group_logger.Rect
        group_logger = StaticBox(
            panel,
            label=self.GUI.text(UI.Main.PANEL_TITLE_SELECTED),
            pos=(rect[0], rect[1] + rect[3] + 20),
            size=(600, 120)
        )
        rect = group_logger.Rect
        lst_selected = CheckListCtrl(
            panel,
            pos=(rect[0] + 10, rect[1] + 20),
            style=LC_REPORT | LC_HRULES | LC_VRULES,
            size=(rect[2] - 20, rect[3] - 30)
        )
        w = lst_selected.Rect[2]
        lst_selected.InsertColumn(col=0, heading=self.GUI.text(UI.Main.SELECTED_LIST_COL_1), width=w * 0.06)
        lst_selected.InsertColumn(col=1, heading=self.GUI.text(UI.Main.SELECTED_LIST_COL_1), width=w * 0)
        lst_selected.InsertColumn(col=2, heading=self.GUI.text(UI.Main.SELECTED_LIST_COL_2), width=w * 0.5)
        lst_selected.InsertColumn(col=3, heading=self.GUI.text(UI.Main.SELECTED_LIST_COL_3), width=w * 0.3)
        lst_selected.InsertColumn(col=4, heading=self.GUI.text(UI.Main.SELECTED_LIST_COL_4), width=w * 0.14)

        self.Service.ctrl_ref['SelectedCourseList'] = lst_selected

        self.GUI.build_menu(self, m.MenuWidget(self, self.Service).menu_data(True))

        """ Control Bar """
        rect = group_logger.Rect
        button_start = Button(
            panel,
            label=self.GUI.text(UI.Main.BUTTON_START_WORK),
            size=(80, 25),
            pos=(rect[2] - 70, rect[1] + rect[3] + 20)
        )
        rect = button_start.Rect
        button_update = Button(
            panel,
            label=self.GUI.text(UI.Main.BUTTON_UPDATE_LIST),
            size=(180, 25),
            pos=(rect[2] + 250, rect[1])
        )
        check_textbook = CheckBox(
            panel,
            NewId(),
            label=self.GUI.text(UI.Main.LABEL_TEXTBOOK),
            pos=(rect[2] + 120, rect[1] + 3)
        )
        self.RemainLabel = StaticText(
            panel,
            label=self.GUI.text(UI.Main.LABEL_CONTACT),
            pos=(15, rect[1] + 3)
        )

        self.Service.ctrl_ref['LaunchButton'] = button_start

        def update_course_layout(data):
            if lst_course.ItemCount > 0:
                lst_course.DeleteAllItems()
            for i, item in enumerate(data):
                lst_course.InsertItem(i, '')
                for j in range(10):
                    lst_course.SetItem(i, j, item[j])

        def on_update_layout(update=False):
            th = threading.Thread(target=self.Service.get_general_elective_courses, args=(update_course_layout, update))
            th.setDaemon(True)
            th.start()

        def on_check_item(index, flag):
            count = lst_course.CheckItemCount()
            if count > Curricula.MAX_SELECTED_CURRICULA:
                lst_course.UnCheckAll()
                lst_course.CheckItem(index, True)

        def on_start():
            checked_name = lst_course.GetCheckedValue(1)
            checked_time = lst_course.GetCheckedValue(7)
            checked_code = lst_course.GetCheckedValue(6)
            checked_key = lst_course.GetCheckedValue(5)
            checked_course_textbook = lst_course.GetCheckedValue(8)
            checked_type = lst_course.GetCheckedValue(9)
            if len(checked_code) == 0:
                GUI.alert_error(
                    self.GUI.text(UI.Main.Dialog.Error.TITLE),
                    self.GUI.text(Msg.Main.NO_WORK_SELECTED)
                )
                return

            if checked_type == ['COMPULSORY']:
                self.Service.value_ref['ExpectedCourseCode'] = [checked_code[0]]
                self.Service.value_ref['ExpectedCourseKey'] = [checked_key[0]]
                self.Service.value_ref['ExpectedCourseTime'] = checked_time
                self.Service.value_ref['ExpectedCourseName'] = checked_name
                self.Service.value_ref['ExpectedCourseTextBookName'] = checked_course_textbook
                self.Service.value_ref['ExpectedCourseType'] = checked_type
            elif checked_type == ['GENERAL_ELECTIVE']:
                self.Service.value_ref['ExpectedCourseCode'] = ['{}xk'.format(checked_code[0])]
                self.Service.value_ref['ExpectedCourseTime'] = checked_time
                self.Service.value_ref['ExpectedCourseName'] = checked_name
                self.Service.value_ref['ExpectedCourseType'] = checked_type
                self.Service.value_ref['ExpectedCourseTextBook'] = ['{}jc'.format(checked_code[0])]
                self.Service.value_ref['ExpectedCourseTextBookName'] = checked_course_textbook
                self.Service.value_ref['ExpectedCourseTextBookCode'] = ['{}jcnr'.format(checked_code[0])]

            if not self.Service.agreement_status and self.Service.login_status:
                GUI.alert_error(
                    self.GUI.text(UI.Main.Dialog.Error.TITLE),
                    self.GUI.text(Msg.Main.NOT_INITIALIZED_YET)
                )
                th = threading.Thread(target=self.Service.agreement)
                th.setDaemon(True)
                th.start()
                return

            if not self.Service.login_validate():
                self.status_bar.SetStatusText(
                    self.GUI.text(Msg.Login.LOGIN_CERTIFICATE_EXPIRED),
                )
                th = threading.Thread(target=self.Service.login_base, args=(on_start, False))
                th.setDaemon(True)
                th.start()

            self.Service.tasks_status = True

            th = threading.Thread(target=self.Service.start_work)
            th.setDaemon(True)
            th.start()

        def drop_course(index, flag):
            param = lst_selected.GetItem(index, 1).GetText()
            name = lst_selected.GetItem(index, 2).GetText()
            if not flag and param:
                answer = MessageBox(
                    self.GUI.text(Msg.Main.DROP_CONFIRM, name),
                    self.GUI.text(Msg.Main.DROP_CONFIRM_TITLE),
                    YES_NO | ICON_INFORMATION
                )

                result = self.Service.drop_course(param) if answer == YES else False
                if not result:
                    lst_selected.CheckItem(index, True)

        def on_compulsory():
            dlg = CompulsoryDlg(service=self.Service)
            dlg.ShowModal()
            dlg.Destroy()

        def search_course():
            lst_course.UnCheckAll()
            keyword = entry_search.GetValue()
            result = []
            first_index = -1
            decoded_course_data = Cache.open(RSAUtils.decrypt(UserConfig().COURSE_DATA, decode=False, local=True))
            for index, item in enumerate(decoded_course_data):

                if keyword in item[1]:
                    if first_index == -1:
                        first_index = index
                    result.append(index)
            if result and len(result) > 0:
                selected_ids = [result[index] for index in range(Curricula.MAX_SELECTED_CURRICULA)]
                for i in selected_ids:
                    lst_course.CheckItem(i, True)
                lst_course.Focus(selected_ids[0])

        self.Bind(EVT_BUTTON, lambda x: on_start(), button_start)
        self.Bind(EVT_BUTTON, lambda x: on_update_layout(True), button_update)

        self.Bind(EVT_BUTTON, lambda x: search_course(), button_search)
        self.Bind(EVT_TEXT_ENTER, lambda x: search_course(), entry_search)

        self.Bind(EVT_BUTTON, lambda x: on_compulsory(), btn_compulsory)
        lst_selected.OnCheckItem = drop_course

        check_textbook.SetValue(True)

        def set_textbook():
            self.Service.has_textbook = check_textbook.Value

        self.Bind(
            EVT_CHECKBOX,
            lambda x: set_textbook(),
            check_textbook
        )

        lst_course.OnCheckItem = on_check_item
        thread = threading.Thread(target=on_update_layout)
        thread.setDaemon(True)
        thread.start()

        # if not self.Service.agreement_status:
        #     thread = threading.Thread(target=self.Service.agreement)
        #     thread.setDaemon(True)
        #     thread.start()

