#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from wx.lib.mixins.listctrl import *
from wx import ListCtrl, ID_ANY, DefaultPosition


class CheckListCtrl(ListCtrl, CheckListCtrlMixin):
    """ TextEditMixin allows any column to be edited. """

    def __init__(self, parent, _id=ID_ANY, pos=DefaultPosition, size=wx.DefaultSize, style=0):
        """Constructor"""
        ListCtrl.__init__(self, parent, _id, pos, size, style)
        CheckListCtrlMixin.__init__(self)

    def CheckItemCount(self):
        return len([i for i in range(self.ItemCount) if self.IsChecked(i)])

    def GetCheckedValue(self, col):
        return [self.GetItem(i, col).GetText() for i in range(self.ItemCount) if self.IsChecked(i)]

    def UnCheckAll(self):
        for i in range(self.ItemCount):
            self.CheckItem(i, False)

    def OnCheckItem(self, index, flag):
        """flag is True if the item was checked, False if unchecked"""
        pass
