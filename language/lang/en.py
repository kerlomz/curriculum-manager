#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from language.base import *
from language.constants import *


class English(Language):
    def __init__(self):
        super(English, self).__init__()
        self.text = {
            UI.Login.TITLE: 'CurriculaMan v*1',
            UI.Login.PANEL_TITLE_LOGIN: 'Log in',
            UI.Login.LABEL_ID: 'StudentID',
            UI.Login.LABEL_PWD: 'Password',
            UI.Login.BUTTON_SUBMIT: 'Log In',
            UI.Login.CHECK_BOX_REMEMBER: 'Remember',
            Msg.Login.LOGIN_CERTIFICATE_EXPIRED: 'Login credentials lost',
            Msg.Login.LOGIN_SUCCESS: 'Login Completed, time consuming: *1',
            Msg.Login.LOGIN_FAILED: 'Logon failure, *1',
            Msg.Login.LOGOUT_SUCCESS: 'Log off successfully',

            UI.Main.TITLE: 'Welcome - *1',

            UI.Main.PANEL_TITLE_SEARCH: 'Search Bar',
            UI.Main.PANEL_TITLE_COURSE: 'Available Course List',
            UI.Main.PANEL_TITLE_LOGGER: 'Operation Logger',
            UI.Main.PANEL_TITLE_SELECTED: 'Selected Courses',
            UI.Main.PANEL_TITLE_ACTION: 'Action',

            UI.Main.BUTTON_LOGOUT: 'Log Out',
            UI.Main.BUTTON_SEARCH: 'Search',
            UI.Main.BUTTON_START_WORK: 'Start',
            UI.Main.BUTTON_UPDATE_LIST: 'Update Course List',
            UI.Main.BUTTON_COMPULSORY: 'Compulsory Course',

            UI.Main.COURSE_LIST_COL_1: 'No',
            UI.Main.COURSE_LIST_COL_2: 'Course Name',
            UI.Main.COURSE_LIST_COL_3: 'School Time',
            UI.Main.COURSE_LIST_COL_4: 'Teacher',
            UI.Main.COURSE_LIST_COL_5: 'Remain',
            UI.Main.COURSE_LIST_COL_6: '*Course Code',
            UI.Main.COURSE_LIST_COL_7: '*Course Key',
            UI.Main.COURSE_LIST_COL_8: '*School Time',
            UI.Main.COURSE_LIST_COL_9: '*TextBook',
            UI.Main.COURSE_LIST_COL_10: '*Type',

            UI.Main.SELECTED_LIST_COL_1: 'No',
            UI.Main.SELECTED_LIST_COL_2: 'Curricula Name',
            UI.Main.SELECTED_LIST_COL_3: 'School Time',
            UI.Main.SELECTED_LIST_COL_4: 'Textbook',

            UI.Main.LOG_LIST_COL_1: 'Count',
            UI.Main.LOG_LIST_COL_2: 'Time',
            UI.Main.LOG_LIST_COL_3: 'Content',

            UI.Main.LABEL_REMAIN: 'Available Credit: *1',
            UI.Main.LABEL_TEXTBOOK: 'Book Textbook',
            UI.Main.LABEL_CONTACT: "QQ Group：137991872",

            UI.Main.Dialog.Donate.TITLE: 'Donate',
            UI.Main.Dialog.Donate.LABEL_DONATE: 'Scan the above QR code with Alipay to support the author',

            UI.Main.Dialog.About.TITLE: 'About Author',
            UI.Main.Dialog.About.INFO_TITLE: 'Information',
            UI.Main.Dialog.About.LABEL_AUTHOR: 'Author:    *1',
            UI.Main.Dialog.About.LABEL_VERSION: 'Version:    *1',
            UI.Main.Dialog.About.LABEL_EMAIL: 'E-mail:',

            UI.Main.Dialog.About.LABEL_INTRODUCTION: 'Introduction',
            UI.Main.Dialog.About.LABEL_LICENSE: 'License',
            UI.Main.Dialog.About.LABEL_OTHERS: 'Other',

            UI.Main.Dialog.Share.TITLE: 'Share Me',
            UI.Main.Dialog.CourseTable.TITLE: 'Curriculum Schedule',

            UI.Main.Dialog.Compulsory.TITLE: 'Compulsory Course',
            UI.Main.Dialog.Compulsory.COURSE_LIST_COL_1: 'Course Code',
            UI.Main.Dialog.Compulsory.COURSE_LIST_COL_2: 'Course Name',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_1: 'No',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_2: 'Course Name',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_3: 'School Time',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_4: 'Teacher',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_5: 'Remain',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_6: '*Course Code',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_7: '*Course Key',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_8: '*School Time',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_9: '*TextBook',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_10: '*Type',

            UI.Main.Dialog.Compulsory.NO_COURSE_PLANNING: 'No course planning',

            UI.Main.Dialog.Compulsory.BUTTON_SELECT: 'Select',
            UI.Main.Dialog.Compulsory.BUTTON_ADD: 'Add',

            UI.Main.Dialog.Compulsory.NO_WORK_SELECTED: "No course selected",
            UI.Main.Dialog.Compulsory.PANEL_TITLE_COURSE_ROOT: "Scheduled elective course list",
            UI.Main.Dialog.Compulsory.PANEL_TITLE_COURSE_DETAIL: "List of specific courses",

            UI.Main.Dialog.Feedback.TITLE: 'Feedback',
            UI.Main.Dialog.Feedback.LABEL_FEEDBACK: 'Feedback',
            UI.Main.Dialog.Feedback.LABEL_TIP_OFFS: 'Tip-offs',
            UI.Main.Dialog.Feedback.BUTTON_SUBMIT: 'Submit',
            UI.Main.Dialog.Feedback.DLG_SUCCESS_TITLE: 'Feedback',
            UI.Main.Dialog.Feedback.DLG_ERROR_TITLE: 'Error',

            Msg.Common.RETRYING: 'Retrying',
            Msg.Common.LOADING: 'Loading',
            Msg.Common.LOADED: 'Completed',

            Msg.Main.CAPTCHA_SERVER_NO_RESP: "Captcha server has no response",

            Msg.Main.SERVER_AUTH_FORGE_DETECTED: 'Authentication failed, Don\'t forge the response',
            Msg.Main.SERVER_AUTH_EXPIRED: 'Server authentication expired',
            Msg.Main.SERVER_AUTH_STATUS_FAILED: 'Cannot get remote configuration, please check the network',

            Msg.Common.SERVER_NO_RESPONSE: 'Server is not responding',
            Msg.Common.SERVER_ERROR: 'Connection failure *1',

            Msg.Main.SETTING_AGREEMENT: 'Confirming of the elective rules',
            Msg.Main.SETTING_AGREEMENT_SUCCESS: 'Confirmation is completed and takes time: *1',
            Msg.Main.GETTING_CSRF_CER: 'Getting CSRF credentials',
            Msg.Main.CSRF_AUTHENTICATING: 'CSRF authentication is in progress',
            Msg.Main.CSRF_AUTHENTICATION_SUCCESS: 'The server certification is done',
            Msg.Main.THREE_SECOND_LIMITED: 'Three seconds anti-refresh',
            Msg.Main.REQUEST_TIMEOUT: 'Request timed out',

            Msg.Common.ERROR_CODE: 'Error code: *1',
            Msg.Common.REQUEST_ERROR_CODE: 'Request error code: *1',

            Msg.Common.NORTH_CAMPUS: 'North Campus',
            Msg.Common.SOUTH_CAMPUS: 'South Campus',
            Msg.Common.ROUTE_METHOD: 'Route Access',
            Msg.Common.LAB_LIBRARY: 'Lab & Library',

            Msg.Main.DOWNLOADING_UPDATE: 'Downloading updates, please wait...',
            Msg.Main.REMAIN_INSUFFICIENT: 'The number of remaining is insufficient: *1',
            Msg.Main.TASK_RUNNING: 'In progress: *1',
            Msg.Main.TIME_CONFLICT: 'Time conflict',
            Msg.Main.NUMBER_EXCEEDS_THE_LIMIT: 'Exceed the limit',
            Msg.Main.NOT_START_TIME: 'Not yet started',
            Msg.Main.TASK_SELECTED: 'Course selected',
            Msg.Main.DROP_CONFIRM_TITLE: 'Drop Course',
            Msg.Main.DROP_CONFIRM: 'Confirm to drop course <*1> ?',
            Msg.Main.HEARTBEAT_FAILED: 'Fail to send heartbeat packet',
            Msg.Main.TASK_INTERRUPTED: 'The task is terminated',
            Msg.Main.UPDATING_CURRICULA_LIST: 'Getting the public course list',
            Msg.Main.UPDATED_CURRICULA_LIST: 'The public course list has been updated',
            Msg.Main.KILLING_WORK: 'Task is terminating',
            Msg.Main.CONTACT_ADMIN: 'Please contact the administrator',
            Msg.Main.NO_WORK_SELECTED: 'No course selected',
            Msg.Main.UP_TO_DATE: 'Current version *1, is up to date',
            Msg.Main.NOT_INITIALIZED_YET: 'The program is not ready',
            Msg.Main.INITIALIZED: 'Ready',
            Msg.Main.DOWNLOAD_FAILED: 'Fail to download *1',
            Msg.Main.DOWNLOAD_SUCCESS: '*1 download successful',
            Msg.Main.MULTI_THREAD_NOT_SUPPORT: 'Multi-threading is not supported',
            Msg.Main.LICENSE_ERROR: "This version has expired or not authorized, \n"
                                    "Please add QQ group: 137991872, \n"
                                    "and contact the group owner to update.",
            Msg.Main.About.INTRODUCTION: 'The original intention of the product in order to make the course easier, '
                                         'aimed at highly automated course selection, '
                                         'Compared to the Key-Wizard, BurpSuite, '
                                         'the advantage of this product is:\n'
                                         '1, Simple: No coding required, Easy to use.\n'
                                         '2, Intelligent: CNN to identify captcha, once login, no longer logout\n'
                                         '3, Independent: start in the background and work at the same time.\n'
                                         'This product is free software, commercial use is forbidden.',

            Msg.Main.About.LICENSE: 'This product is free software, commercial use is forbidden.\n'
                                    'Once discovered and confirmed, We will inform the relevant department\n'
                                    'Abnormal traffic will be automatically forensics, please know.\n',
            Msg.Main.About.OTHERS: 'If you have suggestions and comments can scan the above QR-Code,\n'
                                   ' please contact me with WeChat.',

            Msg.Main.Share.INTRODUCTION: 'Scan the QR code above, share links to Wechat-Moments\n'
                                         'Each click with 1W (About 4 hours) credit\n'
                                         'Or share the link below to your friends\n'
                                         'Each with 3W (About 24 hours) worth of credit for successful download and use',

            Msg.Main.Feedback.SEND_SUCCESS: 'We have received your feedback.',
            Msg.Main.Feedback.NULL_SUBMIT: 'Please don‘t leave blank',

            Msg.Main.VERSION_EXPIRED: 'This version has expired, please go to http://www.lightday.net to download the '
                                      'latest version',

            UI.Main.Menu.Opr.OPERATION: '&Operation',
            UI.Main.Menu.Opr.STOP_WORK: '&Stop Task',
            UI.Main.Menu.Opr.NAT_ROUTE: '&NAT Route',
            UI.Main.Menu.Opr.LOGOUT: '&Log out',
            UI.Main.Menu.Opr.QUIT: '&Quit',

            UI.Main.Menu.Help.HELP: '&Help',
            UI.Main.Menu.Help.FEEDBACK: '&Feedback',
            UI.Main.Menu.Help.CHECK_UPDATE: 'Check &Update',
            UI.Main.Menu.Help.ABOUT: '&About',

            UI.Main.Menu.Mine.MINE: '&Mine',
            UI.Main.Menu.Mine.GET_TIMES: 'Get more &times',
            UI.Main.Menu.Mine.COURSE_TABLE: '&Curriculum Schedule',
            UI.Main.Menu.Mine.DONATE: '&Donate',

            UI.Main.Dialog.Default.TITLE: 'Prompt',
            UI.Main.Dialog.Default.BUTTON_CONFIRM: 'Ok',
            UI.Main.Dialog.Default.BUTTON_CANCEL: 'Cancel',
            UI.Main.Dialog.Default.BUTTON_COPY: 'Copy',

            UI.Main.Dialog.Error.TITLE: 'Error',
        }