#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

LANGUAGE_MAP = {
    'zh_CN': 0x0804,
    'en_US': 0x0409
}
DELIMITER_MAP = {
    0x0804: ', ',
    0x0409: '，'
}


class UI:

    def __init__(self):
        pass

    class Login:
        def __init__(self):
            pass

        TITLE = 1
        PANEL_TITLE_LOGIN = 2

        LABEL_ID = 3
        LABEL_PWD = 4
        CHECK_BOX_REMEMBER = 5
        BUTTON_SUBMIT = 6

    class Main:
        def __init__(self):
            pass

        TITLE = 21
        PANEL_TITLE_SEARCH = 22
        PANEL_TITLE_COURSE = 23
        PANEL_TITLE_LOGGER = 24
        PANEL_TITLE_SELECTED = 25
        PANEL_TITLE_ACTION = 26

        BUTTON_LOGOUT = 26
        BUTTON_SEARCH = 27
        BUTTON_START_WORK = 28
        BUTTON_UPDATE_LIST = 29
        BUTTON_COMPULSORY = 30

        COURSE_LIST_COL_1 = 31
        COURSE_LIST_COL_2 = 32
        COURSE_LIST_COL_3 = 33
        COURSE_LIST_COL_4 = 34
        COURSE_LIST_COL_5 = 35
        COURSE_LIST_COL_6 = 36
        COURSE_LIST_COL_7 = 37
        COURSE_LIST_COL_8 = 38
        COURSE_LIST_COL_9 = 39
        COURSE_LIST_COL_10 = 40

        SELECTED_LIST_COL_1 = 37
        SELECTED_LIST_COL_2 = 38
        SELECTED_LIST_COL_3 = 39
        SELECTED_LIST_COL_4 = 40

        LOG_LIST_COL_1 = 41
        LOG_LIST_COL_2 = 42
        LOG_LIST_COL_3 = 43

        LABEL_REMAIN = 44
        LABEL_TEXTBOOK = 45

        LABEL_CONTACT = 50

        class Menu:
            def __init__(self):
                pass

            class Opr:
                def __init__(self):
                    pass

                OPERATION = 1001
                STOP_WORK = 1002
                NAT_ROUTE = 1003
                LOGOUT = 1004
                QUIT = 1005

            class Mine:
                def __init__(self):
                    pass

                MINE = 1021
                COURSE_TABLE = 1022
                GET_TIMES = 1023
                DONATE = 1024

            class Help:
                def __init__(self):
                    pass

                HELP = 1041
                FEEDBACK = 1042
                ABOUT = 1043
                CHECK_UPDATE = 1044

        class Dialog:
            def __init__(self):
                pass

            class Default:
                def __init__(self):
                    pass

                TITLE = 1201
                BUTTON_CONFIRM = 1202
                BUTTON_CANCEL = 1203
                BUTTON_COPY = 1204

            class Error:
                def __init__(self):
                    pass

                TITLE = 1301

            class About:
                def __init__(self):
                    pass

                TITLE = 1401
                INFO_TITLE = 1402
                LABEL_VERSION = 1403
                LABEL_AUTHOR = 1404
                LABEL_EMAIL = 1405

                LABEL_INTRODUCTION = 1406
                LABEL_LICENSE = 1407
                LABEL_OTHERS = 1408

            class Donate:
                def __init__(self):
                    pass

                TITLE = 1501
                LABEL_DONATE = 1502

            class Share:
                def __init__(self):
                    pass

                TITLE = 1601

            class Feedback:
                def __init__(self):
                    pass

                TITLE = 1701
                LABEL_FEEDBACK = 1702
                LABEL_TIP_OFFS = 1703
                BUTTON_SUBMIT = 1704

                DLG_SUCCESS_TITLE = 1711
                DLG_ERROR_TITLE = 1712

            class CourseTable:
                def __init__(self):
                    pass

                TITLE = 1801

            class Compulsory:

                def __init__(self):
                    pass

                TITLE = 1901
                COURSE_LIST_COL_1 = 1911
                COURSE_LIST_COL_2 = 1912

                COURSE_DETAIL_LIST_COL_1 = 1913
                COURSE_DETAIL_LIST_COL_2 = 1914
                COURSE_DETAIL_LIST_COL_3 = 1915
                COURSE_DETAIL_LIST_COL_4 = 1916
                COURSE_DETAIL_LIST_COL_5 = 1917
                COURSE_DETAIL_LIST_COL_6 = 1918
                COURSE_DETAIL_LIST_COL_7 = 1919
                COURSE_DETAIL_LIST_COL_8 = 1919
                COURSE_DETAIL_LIST_COL_9 = 1919
                COURSE_DETAIL_LIST_COL_10 = 1920

                NO_COURSE_PLANNING = 1921

                BUTTON_SELECT = 1930
                BUTTON_ADD = 1931

                NO_WORK_SELECTED = 1940

                PANEL_TITLE_COURSE_ROOT = 2000
                PANEL_TITLE_COURSE_DETAIL = 2001


class Msg:

    def __init__(self):
        pass

    class Login:
        def __init__(self):
            pass

        LOGIN_CERTIFICATE_EXPIRED = 10001
        LOGIN_SUCCESS = 10002
        LOGIN_FAILED = 10003
        LOGOUT_SUCCESS = 10004
        ONE_DEVICE_MANY_ACCOUNT = 10005

    class Main:
        def __init__(self):
            pass

        SERVER_AUTH_FORGE_DETECTED = 11001
        SERVER_AUTH_EXPIRED = 11002
        SERVER_AUTH_STATUS_FAILED = 11003

        CAPTCHA_SERVER_NO_RESP = 11004
        SETTING_AGREEMENT = 11005
        SETTING_AGREEMENT_SUCCESS = 11006
        GETTING_CSRF_CER = 11007
        CSRF_AUTHENTICATING = 11008
        CSRF_AUTHENTICATION_SUCCESS = 11009
        TASK_RUNNING = 11010
        TIME_CONFLICT = 11011
        NUMBER_EXCEEDS_THE_LIMIT = 11012
        NOT_START_TIME = 11013
        TASK_SELECTED = 11014
        DROP_CONFIRM = 11015
        DROP_CONFIRM_TITLE = 11016
        HEARTBEAT_FAILED = 11017
        TASK_INTERRUPTED = 11018
        KILLING_WORK = 11019
        DOWNLOADING_UPDATE = 11020
        UPDATING_CURRICULA_LIST = 11021
        UPDATED_CURRICULA_LIST = 11022

        REQUEST_TIMEOUT = 11023
        CONTACT_ADMIN = 11024

        NOT_INITIALIZED_YET = 11025
        THREE_SECOND_LIMITED = 11026

        REMAIN_INSUFFICIENT = 11027

        VERSION_EXPIRED = 11028
        UP_TO_DATE = 11029

        INITIALIZED = 11030
        NO_WORK_SELECTED = 11031

        DOWNLOAD_FAILED = 11032
        DOWNLOAD_SUCCESS = 11033
        MULTI_THREAD_NOT_SUPPORT = 11034

        LICENSE_ERROR = 11035

        class About:
            def __init__(self):
                pass

            INTRODUCTION = 11101
            LICENSE = 11102
            OTHERS = 11103

        class Share:
            def __init__(self):
                pass

            INTRODUCTION = 11201

        class Feedback:
            def __init__(self):
                pass

            SEND_SUCCESS = 11301
            NULL_SUBMIT = 11302

    class Common:
        def __init__(self):
            pass

        SERVER_NO_RESPONSE = 12001
        SERVER_ERROR = 12002
        RETRYING = 12003
        LOADING = 12004
        LOADED = 12005
        ERROR_CODE = 12006
        REQUEST_ERROR_CODE = 12007

        NORTH_CAMPUS = 13001
        SOUTH_CAMPUS = 13002
        ROUTE_METHOD = 13003
        LAB_LIBRARY = 13004
