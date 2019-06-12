#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import re
import threading
from wx import *
from widget.check_list_ctrl import CheckListCtrl
from utils import *
from language.constants import *


class CompulsoryDlg(Dialog):
    def __init__(self, parent=None, service=None):
        self.GUI = GUI(self, SystemConfig.LANGUAGE)
        Dialog.__init__(
            self,
            parent=parent,
            size=(640, 600)
        )
        self.Service = service
        self.Service.update_compulsory_courses()
        self.Title = self.GUI.text(UI.Main.Dialog.Compulsory.TITLE)
        self.info()

    def info(self):

        panel = Panel(self, NewId())

        rect = self.GetClientRect()
        """ Search Bar """
        group_search = StaticBox(
            panel,
            label=self.GUI.text(UI.Main.PANEL_TITLE_SEARCH),
            pos=(rect[0] + 10, rect[1] + 10),
            size=(600, 60)
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

        """ Course List """
        rect = group_search.Rect
        group_course = StaticBox(
            panel,
            label=self.GUI.text(UI.Main.Dialog.Compulsory.PANEL_TITLE_COURSE_ROOT),
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
        lst_course.InsertColumn(
            col=0, heading=self.GUI.text(UI.Main.Dialog.Compulsory.COURSE_LIST_COL_1), width=w * 0.3
        )
        lst_course.InsertColumn(
            col=1, heading=self.GUI.text(UI.Main.Dialog.Compulsory.COURSE_LIST_COL_2), width=w * 0.6
        )

        self.Bind(EVT_BUTTON, lambda x: search_course(), button_search)
        self.Bind(EVT_TEXT_ENTER, lambda x: search_course(), entry_search)

        def update_course_layout(data):
            if lst_course.ItemCount > 0:
                lst_course.DeleteAllItems()
            for i, item in enumerate(data):
                lst_course.InsertItem(i, '')
                lst_course.SetItem(i, 0, item[0])
                lst_course.SetItem(i, 1, item[1])

        thread = threading.Thread(target=update_course_layout, args=(self.Service.compulsory_course_list, ))
        thread.setDaemon(True)
        thread.start()

        def search_course():
            lst_course.UnCheckAll()
            keyword = entry_search.GetValue()
            result = []
            first_index = -1

            for index, item in enumerate(self.Service.compulsory_course_list):
                if keyword in item[1]:
                    if first_index == -1:
                        first_index = index
                    result.append(index)
            if result and len(result) > 0:
                selected_ids = [result[index] for index in range(Curricula.MAX_SELECTED_CURRICULA)]
                for i in selected_ids:
                    lst_course.CheckItem(i, True)
                lst_course.Focus(selected_ids[0])
            self.Service.get_specified_compulsory_course(
                update_course_layout, lst_course.GetCheckedValue(0)
            )

        def on_check_item(index, flag):
            count = lst_course.CheckItemCount()
            if count > Curricula.MAX_SELECTED_CURRICULA:
                lst_course.UnCheckAll()
                lst_course.CheckItem(index, True)

        lst_course.OnCheckItem = on_check_item

        rect = group_course.Rect
        StaticBox(
            panel,
            label=self.GUI.text(UI.Main.Dialog.Compulsory.PANEL_TITLE_COURSE_DETAIL),
            pos=(rect[0], rect[1] + rect[3] + 50),
            size=(600, 180)
        )

        lst_selected = CheckListCtrl(
            panel,
            pos=(rect[0] + 10, rect[1] + 250),
            style=LC_REPORT | LC_HRULES | LC_VRULES,
            size=(rect[2] - 20, rect[3] - 30)
        )

        w = lst_selected.Rect[2]
        for i, ratio in enumerate([0.06, 0.35, 0.3, 0.15, 0.1, 0, 0, 0, 0, 0]):
            lst_selected.InsertColumn(
                col=i+1,
                heading=self.GUI.text(UI.Main.Dialog.Compulsory().__getattribute__('COURSE_DETAIL_LIST_COL_{}'.format(i+1))),
                width=w * ratio
            )

        button_select = Button(
            panel,
            label=self.GUI.text(UI.Main.Dialog.Compulsory.BUTTON_SELECT),
            size=(80, 25),
            pos=(rect[2] - 80, rect[1] + 200)
        )

        self.Bind(
            EVT_BUTTON, lambda x: self.Service.get_specified_compulsory_course(
                update_course_layout, lst_course.GetCheckedValue(0)
            ),
            button_select
        )

        def update_course_layout(data):
            if lst_selected.ItemCount > 0:
                lst_selected.DeleteAllItems()
            for i, item in enumerate(data):
                course_time_mini = re.sub("{.+?}", "", item['CourseTime'])
                lst_selected.InsertItem(i, '')
                lst_selected.SetItem(i, 0, '')
                lst_selected.SetItem(i, 1, item['CourseName'])
                lst_selected.SetItem(i, 2, course_time_mini)
                lst_selected.SetItem(i, 3, item['Teacher'])
                lst_selected.SetItem(i, 4, str(item['Capacity'] - item['Selected']))
                lst_selected.SetItem(i, 5, item['CourseCode'])
                lst_selected.SetItem(i, 6, item['CourseKey'])
                lst_selected.SetItem(i, 7, item['CourseTime'])
                lst_selected.SetItem(i, 8, '')
                lst_selected.SetItem(i, 9, 'COMPULSORY')

        button_select_detail = Button(
            panel,
            label=self.GUI.text(UI.Main.Dialog.Compulsory.BUTTON_ADD),
            size=(80, 25),
            pos=(rect[2] - 80, rect[1] + 420)
        )

        def get_selected_course():
            if not lst_selected.GetCheckedValue(1):
                GUI.alert_error(
                    self.GUI.text(UI.Main.Dialog.Error.TITLE),
                    self.GUI.text(Msg.Main.NO_WORK_SELECTED)
                )
                return

            keys = [
                'No', 'CourseName', 'MniSchoolTime', 'Teacher', 'Remain',
                'CourseCode', 'CourseKey', 'SchoolTime', 'TextBook', 'Type'
            ]
            return [{key: lst_selected.GetCheckedValue(index)[0] for index, key in enumerate(keys)}]

        self.Bind(
            EVT_BUTTON, lambda x: self.Service.insert_optional_course(get_selected_course()),
            button_select_detail
        )


if __name__ == '__main__':
    app = App(False)
    aboutDlg = CompulsoryDlg()
    aboutDlg.ShowModal()
