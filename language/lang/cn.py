#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
from language.base import *
from language.constants import *


class Chinese(Language):
    def __init__(self):
        super(Chinese, self).__init__()
        self.text = {
            UI.Login.TITLE: '课君（城院专版） v*1',
            UI.Login.PANEL_TITLE_LOGIN: '登陆',
            UI.Login.LABEL_ID: '学　号',
            UI.Login.LABEL_PWD: '密　码',
            UI.Login.CHECK_BOX_REMEMBER: '记住密码',
            UI.Login.BUTTON_SUBMIT: '登陆',
            Msg.Login.LOGIN_CERTIFICATE_EXPIRED: '登录凭证失效',
            Msg.Login.LOGIN_SUCCESS: '完成登录请求，共耗时：*1',
            Msg.Login.LOGIN_FAILED: '登录失败，*1',
            Msg.Login.LOGOUT_SUCCESS: '注销成功',
            Msg.Login.ONE_DEVICE_MANY_ACCOUNT:  '疑似非法登陆，有异议请联系管理员',

            UI.Main.TITLE: '欢迎使用 - *1',

            UI.Main.PANEL_TITLE_SEARCH: '搜索栏',
            UI.Main.PANEL_TITLE_COURSE: '可选课程列表',
            UI.Main.PANEL_TITLE_LOGGER: '操作日志',
            UI.Main.PANEL_TITLE_SELECTED: '已选课程',
            UI.Main.PANEL_TITLE_ACTION: '操作',


            UI.Main.BUTTON_LOGOUT: '注销',
            UI.Main.BUTTON_SEARCH: '搜索',
            UI.Main.BUTTON_START_WORK: '选课',
            UI.Main.BUTTON_UPDATE_LIST: '更新公选列表',
            UI.Main.BUTTON_COMPULSORY: '必修/限选课',

            UI.Main.COURSE_LIST_COL_1: '序号',
            UI.Main.COURSE_LIST_COL_2: '课程名称',
            UI.Main.COURSE_LIST_COL_3: '课程时间',
            UI.Main.COURSE_LIST_COL_4: '教师',
            UI.Main.COURSE_LIST_COL_5: '余量',
            UI.Main.COURSE_LIST_COL_6: '*课程号',
            UI.Main.COURSE_LIST_COL_7: '*选课号',
            UI.Main.COURSE_LIST_COL_8: '*课程时间',
            UI.Main.COURSE_LIST_COL_9: '*教材预定',
            UI.Main.COURSE_LIST_COL_10: '*类别',

            UI.Main.SELECTED_LIST_COL_1: '序号',
            UI.Main.SELECTED_LIST_COL_2: '课程名称',
            UI.Main.SELECTED_LIST_COL_3: '上课时间',
            UI.Main.SELECTED_LIST_COL_4: '教材预定',

            UI.Main.LABEL_REMAIN: '您的可用额度为：*1',
            UI.Main.LABEL_TEXTBOOK: '预订教材',
            UI.Main.LABEL_CONTACT: "官方指定QQ群：137991872",

            UI.Main.LOG_LIST_COL_1: '次数',
            UI.Main.LOG_LIST_COL_2: '时间',
            UI.Main.LOG_LIST_COL_3: '日志内容',

            UI.Main.Dialog.Donate.TITLE: '赞助',
            UI.Main.Dialog.Donate.LABEL_DONATE: '支付宝扫描上面二维码赞助作者',

            UI.Main.Dialog.About.TITLE: '关于',
            UI.Main.Dialog.About.INFO_TITLE: '信息',
            UI.Main.Dialog.About.LABEL_AUTHOR: '作者:    Mr.Zhou',
            UI.Main.Dialog.About.LABEL_VERSION: '版本:    *1',
            UI.Main.Dialog.About.LABEL_EMAIL: 'E-mail:',

            UI.Main.Dialog.About.LABEL_INTRODUCTION: '介绍',
            UI.Main.Dialog.About.LABEL_LICENSE: '协议',
            UI.Main.Dialog.About.LABEL_OTHERS: '其他',

            UI.Main.Dialog.Share.TITLE: '分享我',

            UI.Main.Dialog.CourseTable.TITLE: '个人课表',

            UI.Main.Dialog.Compulsory.TITLE: '专业课选择',
            UI.Main.Dialog.Compulsory.COURSE_LIST_COL_1: '课程号',
            UI.Main.Dialog.Compulsory.COURSE_LIST_COL_2: '课程名称',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_1: '序号',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_2: '课程名称',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_3: '课程时间',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_4: '教师',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_5: '余量',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_6: '*课程号',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_7: '*选课号',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_8: '*课程时间',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_9: '*教材预定',
            UI.Main.Dialog.Compulsory.COURSE_DETAIL_LIST_COL_10: '*类别',

            UI.Main.Dialog.Compulsory.NO_COURSE_PLANNING: '没有课程计划',

            UI.Main.Dialog.Compulsory.BUTTON_SELECT: '选定',
            UI.Main.Dialog.Compulsory.BUTTON_ADD: '添加',

            UI.Main.Dialog.Compulsory.NO_WORK_SELECTED: "未选择课程",
            UI.Main.Dialog.Compulsory.PANEL_TITLE_COURSE_ROOT: "计划内选课列表",
            UI.Main.Dialog.Compulsory.PANEL_TITLE_COURSE_DETAIL: "具体课时列表",

            UI.Main.Dialog.Feedback.TITLE: '反馈',
            UI.Main.Dialog.Feedback.LABEL_FEEDBACK: '反馈',
            UI.Main.Dialog.Feedback.LABEL_TIP_OFFS: '举报',
            UI.Main.Dialog.Feedback.BUTTON_SUBMIT: '提交',
            UI.Main.Dialog.Feedback.DLG_SUCCESS_TITLE: '提交成功',
            UI.Main.Dialog.Feedback.DLG_ERROR_TITLE: '提交失败',

            Msg.Common.RETRYING: '正在重试',
            Msg.Common.LOADING: '加载中',
            Msg.Common.LOADED: '加载完成',

            Msg.Main.CAPTCHA_SERVER_NO_RESP: "识码服务器未响应",

            Msg.Main.SERVER_AUTH_FORGE_DETECTED: '服务器认证失败，请勿伪造响应内容',
            Msg.Main.SERVER_AUTH_EXPIRED: '服务器认证过期',
            Msg.Main.SERVER_AUTH_STATUS_FAILED: '无法获取远程配置，请检查网络',

            Msg.Common.SERVER_NO_RESPONSE: '服务器未响应',
            Msg.Common.SERVER_ERROR: '连接服务器失败，*1',

            Msg.Main.SETTING_AGREEMENT: '选课规则同意确认中，请耐心等待',
            Msg.Main.SETTING_AGREEMENT_SUCCESS: '规则确认完成，共耗时：*1',
            Msg.Main.GETTING_CSRF_CER: '正在获取跨站身份凭证',
            Msg.Main.CSRF_AUTHENTICATING: '正在进行跨站身份认证',
            Msg.Main.CSRF_AUTHENTICATION_SUCCESS: '完成服务器认证',
            Msg.Main.THREE_SECOND_LIMITED: '三秒防刷',
            Msg.Main.REQUEST_TIMEOUT: '请求超时',

            Msg.Common.ERROR_CODE: '错误代码：*1',
            Msg.Common.REQUEST_ERROR_CODE: '请求错误代码：*1',

            Msg.Common.NORTH_CAMPUS: '北校寝室',
            Msg.Common.SOUTH_CAMPUS: '南校寝室',
            Msg.Common.ROUTE_METHOD: '路由接入',
            Msg.Common.LAB_LIBRARY: '机房、图书馆',

            Msg.Main.DOWNLOADING_UPDATE: '正在下载更新，请稍等',
            Msg.Main.REMAIN_INSUFFICIENT: '剩余可用次数不足，当前可用为：*1',
            Msg.Main.TASK_RUNNING: '正在进行选课：*1',
            Msg.Main.TIME_CONFLICT: '时间冲突',
            Msg.Main.NUMBER_EXCEEDS_THE_LIMIT: '人数超过限制',
            Msg.Main.NOT_START_TIME: '尚未开始选课',
            Msg.Main.TASK_SELECTED: '课程已选上',
            Msg.Main.DROP_CONFIRM_TITLE: '退课',
            Msg.Main.DROP_CONFIRM: '确认退选 《*1》 ？',
            Msg.Main.HEARTBEAT_FAILED: '心跳包发送失败',
            Msg.Main.TASK_INTERRUPTED: '任务已终止',
            Msg.Main.UPDATING_CURRICULA_LIST: '正在获取公选列表',
            Msg.Main.UPDATED_CURRICULA_LIST: '公选列表已更新',
            Msg.Main.KILLING_WORK: '正在结束任务',
            Msg.Main.CONTACT_ADMIN: '请联系管理员',
            Msg.Main.NO_WORK_SELECTED: '没有选择课程',
            Msg.Main.UP_TO_DATE: '当前版本 *1，已是最新版',
            Msg.Main.NOT_INITIALIZED_YET: '程序未就绪',
            Msg.Main.INITIALIZED: '准备就绪',
            Msg.Main.DOWNLOAD_FAILED: '下载 *1 失败',
            Msg.Main.DOWNLOAD_SUCCESS: '*1 下载完成',
            Msg.Main.MULTI_THREAD_NOT_SUPPORT: '不支持多线程',
            Msg.Main.LICENSE_ERROR: "此版本已过期或未授权，请加QQ群：137991872，联系群主更新。",
            Msg.Main.About.INTRODUCTION: '该产品初衷为了解决一课难求的问题，旨在通过自动化技术实现自动选课，'
                                         '相较于按键精灵、BurpSuite，本产品的优势在于：\n'
                                         '1、傻瓜式：没有复杂和多余的操作，一看就懂\n'
                                         '2、智能化：基于CNN识别验证码，智能重试，一次登陆，不再掉线\n'
                                         '3、独立性：挂机式，选课与工作并行，互不干扰\n'
                                         '本产品为免费软件，禁止将本软件用于商业盈利',
            Msg.Main.About.LICENSE: '本软件免费，禁止将本软件用于商业盈利（如售卖课程）'
                                    '\n一经发现并核实，将列入黑名单，并上报相关部门'
                                    '\n后台若判定为异常流量将自动取证，请悉知',
            Msg.Main.About.OTHERS: '如有建议与意见可以扫描上面的二维码加我微信，乐意为您效劳',

            Msg.Main.Share.INTRODUCTION: '扫描上面二维码，分享链接至朋友圈'
                                         '\n好友点击即可增加5K（约4小时）额度。'
                                         '\n或将下面链接分享给好友'
                                         '\n每个成功下载并使用即可获得3W（约24小时）额度',

            Msg.Main.Feedback.SEND_SUCCESS: '我们已经收到您的反馈了！',
            Msg.Main.Feedback.NULL_SUBMIT: '请勿留空',

            Msg.Main.VERSION_EXPIRED: '该版本已过期，请到 http://www.lightday.net 下载最新版',

            UI.Main.Menu.Opr.OPERATION: '操作(&O)',
            UI.Main.Menu.Opr.STOP_WORK: '停止任务(&S)',
            UI.Main.Menu.Opr.NAT_ROUTE: '内网穿透(&N)',
            UI.Main.Menu.Opr.LOGOUT: '注销(&L)',
            UI.Main.Menu.Opr.QUIT: '退出(&Q)',

            UI.Main.Menu.Help.HELP: '帮助(&H)',
            UI.Main.Menu.Help.FEEDBACK: '反馈(&F)',
            UI.Main.Menu.Help.CHECK_UPDATE: '检查更新(&U)',
            UI.Main.Menu.Help.ABOUT: '关于(&A)',

            UI.Main.Menu.Mine.MINE: '个人中心(&M)',
            UI.Main.Menu.Mine.GET_TIMES: '获取额度(&T)',
            UI.Main.Menu.Mine.COURSE_TABLE: '个人课表(&C)',
            UI.Main.Menu.Mine.DONATE: '捐赠(&D)',

            UI.Main.Dialog.Default.TITLE: '提示',
            UI.Main.Dialog.Default.BUTTON_CONFIRM: '确认',
            UI.Main.Dialog.Default.BUTTON_CANCEL: '取消',
            UI.Main.Dialog.Default.BUTTON_COPY: '复制',

            UI.Main.Dialog.Error.TITLE: '错误',

        }
