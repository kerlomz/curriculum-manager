#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import re
import json
import struct
import random
import urllib3
import asyncio
import threading
from interface import Interface
from parsel import *
from utils import *
from fake_useragent import UserAgent
from requests import utils
from concurrent.futures import ThreadPoolExecutor
from verification import GoogleRPC


class Service(object):
    def __init__(self):
        self.parent = None
        self.GUI = None
        self.status_bar = None
        self.ua = UserAgent()
        self.executor = ThreadPoolExecutor(max_workers=50)
        self.dynamic_code = ""
        self.login_session = Session()
        self.action_session = Session()
        self.csrf_token = {
            "Login": '',
            "GeneralElectiveCourseList": '',
            "GeneralElectiveCoursePost": '',
            "CompulsoryCoursePage": '',
            "CompulsoryCourseList": '',
            "CompulsoryCoursePost": '',
        }
        self.request = Network()
        self.captcha = None
        self.captcha_api = Interface()
        self.agreement_status = False
        self.login_status = False
        self.student_code = None
        self.password = None
        self.fullname = None
        self.major_name = ""
        self.tasks_status = True
        self.task_running = False
        self.disabled = False
        self.has_textbook = True
        self.account_status = 'active'
        self.version_status = True
        self.device_status = True
        self.user_group = ''
        self.logger_count = 0
        self.cookies = {}
        self.login_times = 0
        self.ctrl_ref = {
            'SelectedCourseList': None,
            'ExpectedCourseList': None,
            'LoggerList': None,
            'LaunchButton': None
        }
        self.value_ref = {
            'ExpectedCourseCode': [],
            'ExpectedCourseName': [],
            'ExpectedCourseTextBook': [],
            'ExpectedCourseTextBookName': [],
            'ExpectedCourseTextBookCode': [],
            'ExpectedCourseTime': [],
            'ExpectedCourseKey': [],
            'ExpectedCourseType': [],
        }
        self.value_map = {
            'SelectedCourse': []
        }
        self.extension_course_map = {}
        self.compulsory_course_list = []

    def init(self, parent, gui, status_bar):
        self.parent = parent
        self.GUI = gui
        self.status_bar = status_bar
        self.login_session.headers.update({"User-Agent": self.ua.random})
        self.action_session.headers.update({"User-Agent": self.ua.random})

    def login_validate(self, raw_cookie=None):
        """登陆状态校验操作"""
        if raw_cookie:
            self.cookies = raw_cookie if raw_cookie else self.cookies
            self.action_session.cookies = self.cookies

        url = self.request.get_main_url(self.dynamic_code, self.student_code)

        response = Session().get(url, headers=self.login_session.headers, cookies=self.cookies)

        if response is None:
            self.status_bar.SetStatusText(self.GUI.text(Msg.Common.SERVER_NO_RESPONSE))
            return self.login_validate()
        html = Selector(response.text)
        fullname = html.xpath('//span[@id="xhxm"]/text()').extract_first()

        if fullname:
            self.fullname = fullname.replace('同学', '')
            return True
        else:
            return False

    def set_redirect(self):
        """SESSION 重定向操作"""
        redirect = self.login_session.get(url='http://{}'.format(NetworkConfig.HOST_SERVER))
        if not redirect:
            self.status_bar.SetStatusText(self.GUI.text(Msg.Common.SERVER_NO_RESPONSE))
            return self.set_redirect()
        html = Selector(redirect.text)
        self.dynamic_code = re.search('(?<=\().*?(?=\))', redirect.url)
        self.dynamic_code = self.dynamic_code.group() if self.dynamic_code else ""

        self.csrf_token.update({"Login": html.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()})
        self.get_captcha()

    def get_captcha(self, retry=0):
        """识别验证码操作"""
        login_captcha_url = self.request.get_captcha_url(self.dynamic_code)
        resp = self.login_session.get(login_captcha_url)
        image_bytes = resp.content

        captcha_code = self.captcha_api.remote_predict(image_bytes)

        if not captcha_code:
            self.get_captcha(retry+1)

        if retry >= 3:
            print("retry captcha {}".format(retry))
            self.status_bar.SetStatusText(self.GUI.text(Msg.Main.CAPTCHA_SERVER_NO_RESP))
            return

        self.captcha = captcha_code

    def set_login(self, uid, pwd, dynamic_code=None):
        self.student_code = uid
        self.password = pwd
        self.dynamic_code = dynamic_code if dynamic_code else self.dynamic_code

    def login_base(self, func=None, param=True, **kwargs):
        """登陆操作"""

        self.login_status = False
        self.agreement_status = False
        self.tasks_status = True

        self.status_bar.SetStatusText(
            self.GUI.text([Msg.Login.LOGIN_CERTIFICATE_EXPIRED, Msg.Common.RETRYING])
            if self.login_times > 0
            else ''
        )
        self.set_redirect()
        login_url = self.request.get_login_url(self.dynamic_code)
        params = Network.get_login_params(self.student_code, self.password, self.captcha, self.csrf_token['Login'])

        response = self.login_session.post(url=login_url, data=params)

        if response is None:
            self.status_bar.SetStatusText(self.GUI.text(Msg.Common.SERVER_NO_RESPONSE))
            return self.login_base(func=func, param=param, **kwargs)

        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Login.LOGIN_SUCCESS, response.elapsed.microseconds / 1000000)
        )
        response.encoding = "gbk"
        html = Selector(response.text)
        name = html.xpath('//span[@id="xhxm"]/text()').extract_first()
        self.fullname = name.replace('同学', '') if name else None

        message = html.xpath('//script[contains(text(), "alert")]/text()').extract_first()
        message = re.search("(?<=alert\(').*?(?='\))", message).group() if message else None
        title = html.xpath('//title/text()').extract_first()
        error_type = -1 if message and '验证码' in message else 1
        # TODO 逻辑错误，炸网没考虑
        if title:

            # 登陆失败
            if '请登录' in title:
                self.status_bar.SetStatusText(
                    self.GUI.text(Msg.Login.LOGIN_FAILED, message)
                    if self.login_times > 0
                    else ''
                )

                if error_type == -1:
                    print('-1')
                    # print(response.text)
                    # TODO 告知后端
                    # self.report(message='-1 LOGIN TAG', level=3, branch='LOGIN', img=Logger.grab_screen())
                    return self.login_base(func=func, param=param, **kwargs)

            # 登陆成功
            elif '正方教务管理系统' in title:
                self.login_status = True
                print('Logged in!')

                ConfigIO.update(
                    "Certificate",
                    "Account",
                    value=RSAUtils.encrypt(Cache.save([self.student_code, self.password]), local=True)
                )

                # 保存当前 Cookie 字典
                cookie_dict = utils.dict_from_cookiejar(self.login_session.cookies)
                self.cookies = utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
                # 持久化 CookieJar
                ConfigIO.update(
                    "Certificate",
                    "Session",
                    value=RSAUtils.encrypt(Cache.save(self.cookies), local=True)
                )
                # 导入登陆 CookieJar 到 操作会话 (Action Session)
                self.action_session.cookies = self.cookies
                # 持久化 DynamicCode
                ConfigIO.update(
                    "Certificate",
                    "DynamicCode",
                    value=RSAUtils.encrypt(Cache.save(self.dynamic_code), local=True)
                )
                self.agreement()
                if func:
                    if param:
                        func(**kwargs)
                    else:
                        func()
                self.login_times += 1

            else:
                if error_type == -2:
                    print(response.text)
                    return self.login_base(func=func, param=param, **kwargs)
        else:
            message = response.text
            self.login_status = False

        return {"message": message, "status": self.login_status}

    def agreement(self):
        """选课条款同意操作"""

        if self.agreement_status:
            print('已获取同意选课授权.')
            return

        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.SETTING_AGREEMENT)
        )

        general_elective_params = {
            "Button1": "我已认真阅读，并同意以上内容".encode("gbk"),
            "TextBox1": "100",
            "__VIEWSTATE": ViewState.GeneralElectiveAgreement
        }

        compulsory_params = {
            "Button1": "我已认真阅读，并同意以上内容".encode("gbk"),
            "TextBox1": "0",
            "__VIEWSTATE": ViewState.CompulsoryAgreement
        }

        general_elective_action = self.request.get_url(
            self.dynamic_code,
            StaticPath.Request.GENERAL_ELECTIVE_AGREEMENT_PATH,
            dict(xh=self.student_code)
        )

        compulsory_action = self.request.get_url(
            self.dynamic_code,
            StaticPath.Request.COMPULSORY_AGREEMENT_PATH,
            dict(xh=self.student_code)
        )
        referer = self.request.get_main_url(self.dynamic_code, self.student_code)
        self.action_session.headers.update({"Referer": referer})
        general_elective_response = self.action_session.post(url=general_elective_action, data=general_elective_params)
        self.action_session.headers.update({"Referer": referer})
        compulsory_csrf_response = self.action_session.post(url=compulsory_action, data=compulsory_params)

        general_elective_response.encoding = "gbk"
        compulsory_csrf_response.encoding = "gbk"

        if general_elective_response.status_code == 404:
            print(general_elective_response.text)
            print(general_elective_response.url)

        if compulsory_csrf_response.status_code == 404:
            print(compulsory_csrf_response.text)
            print(compulsory_csrf_response.url)

        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.SETTING_AGREEMENT_SUCCESS, general_elective_response.elapsed.microseconds / 1000000 + 4)
        )

        general_elective_html = Selector(general_elective_response.text)
        compulsory_html = Selector(compulsory_csrf_response.text)

        self.major_name = compulsory_html.xpath('//input[@name="zymc"]/@value').extract_first('')
        general_elective_fetched = general_elective_html.xpath('//form[@name="xsyxxxk_form"]/@action').extract_first()
        general_elective_fetched = True if general_elective_fetched else False

        compulsory_fetched = compulsory_html.xpath('//form[@name="xsxk_form"]/@action').extract_first()
        compulsory_fetched = True if compulsory_fetched else False

        self.value_map['SelectedCourse'] = self.parse_selected_course(general_elective_response)
        CheckListUtils.insert(
            self.ctrl_ref['SelectedCourseList'],
            self.value_map['SelectedCourse'],
            ['No', 'DropEvent', 'CourseName', 'CourseTime', 'Textbook']
        )
        general_elective_status = True if general_elective_fetched else False
        compulsory_status = True if compulsory_fetched else False

        self.agreement_status = general_elective_status and compulsory_status
        print(self.agreement_status)

        general_elective_csrf_token = general_elective_html.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()
        compulsory_csrf_token = compulsory_html.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()

        self.csrf_token.update({"GeneralElectiveCourseList": general_elective_csrf_token})
        self.csrf_token.update({"CompulsoryCoursePage": compulsory_csrf_token})
        ConfigIO.update(
            "Cache",
            "CSRF",
            value=RSAUtils.encrypt(Cache.save(self.csrf_token), local=True)
        )

    def fetch_extension_course_map(self):

        extension_course_action = self.request.get_url(
            self.dynamic_code,
            StaticPath.Request.COMPULSORY_LIST_PATH,
            dict(xh=self.student_code, xm="", sm=1)
        )
        extension_course_params = {
            "Button3": "大学英语拓展课".encode("gbk"),
            "__VIEWSTATE": self.csrf_token['CompulsoryCoursePage'],
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "xx": "",
            "zymc": self.major_name.encode("gbk"),
        }
        self.action_session.headers.update({"Referer": extension_course_action})
        extension_course_response = self.action_session.post(url=extension_course_action, data=extension_course_params)
        extension_course_response.encoding = "gbk"

        html = Selector(extension_course_response.text)

        tr_title = html.xpath('//table[@id="kcmcgrid"]/tr[@class="datelisthead"]/td').xpath('string(.)').extract()
        course_title = {selected: i + 1 for i, selected in enumerate(tr_title)}

        tr = html.xpath('//table[@id="kcmcgrid"]/tr[not(@class="datelisthead")]')
        for tr_item in tr:
            onclick = tr_item.xpath('td[{}]/a/@onclick'.format(course_title['课程代码'])).extract_first('')
            course_code = tr_item.xpath('td[{}]/a/text()'.format(course_title['课程代码'])).extract_first('')
            course_name = tr_item.xpath('td[{}]/a/text()'.format(course_title['课程名称'])).extract_first('')
            course_key = re.search("(?<=xkkh=).+?(?=&xh)", onclick)
            course_key = course_key.group() if course_key else None
            self.extension_course_map[course_code] = {"key": course_key, "name": course_name}

    def insert_optional_course(self, data=None):
        """将选中必修课插入到主界面列表中"""
        CheckListUtils.insert(
            self.ctrl_ref['ExpectedCourseList'],
            data,
            [
                'No', 'CourseName', 'MniSchoolTime', 'Teacher', 'Remain',
                'CourseCode', 'CourseKey', 'SchoolTime', 'TextBook', 'Type'
            ],
            clear=False,
            focus=True
        )

    def get_course_table(self):
        """获取当前课程表"""
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        if 5 <= month <= 10:
            stu_year = "{}-{}".format(year, year + 1)
            stu_term = 1
        elif 12 >= month > 10:
            stu_year = "{}-{}".format(year - 1, year)
            stu_term = 2
        elif 1 <= month < 5:
            stu_year = "{}-{}".format(year - 1, year)
            stu_term = 2
        else:
            GUI.alert_error(
                self.GUI.text(UI.Main.Dialog.Error.TITLE),
                self.GUI.text(Msg.Main.NOT_INITIALIZED_YET)
            )
            return
        action = self.request.get_course_table_url(self.dynamic_code, self.student_code, stu_year, stu_term)
        response = self.action_session.get(action)
        response.encoding = "gbk"
        source_code = response.text
        html = Selector(source_code)
        table = html.xpath('//table[@id="Table1"]').extract()
        table = "".join(table)
        style = "<style>table{ background:#000;}table tr td{ background:#fff;}</style>"

        return style + table

    def get_specified_compulsory_course(self, callback, course_code, retry=0):
        """
        获取具体必修课列表
        :param callback:
        :param course_code:
        :param retry:
        :return:
        """
        if retry > 5:
            return

        course_code = course_code[0] if len(course_code) > 0 else None
        if not course_code:
            GUI.alert_error(
                self.GUI.text(UI.Main.Dialog.Error.TITLE),
                self.GUI.text(Msg.Main.NO_WORK_SELECTED)
            )
            return

        action_search = self.request.get_compulsory_search_url(self.dynamic_code, self.student_code)
        detail_action = self.request.get_compulsory_courses_url(self.dynamic_code, self.student_code, self.fullname)

        if course_code in self.extension_course_map:
            result = self.specified_compulsory_course_search(
                detail_action,
                course_code,
                self.extension_course_map[course_code]['name'],
                self.extension_course_map[course_code]['key']
            )
            callback(result)
            return result

        self.action_session.headers.update({"Referer": action_search})
        params_search = self.request.get_compulsory_course_search_params(course_code)
        try:
            response_course = self.action_session.post(action_search, data=params_search)
        except Exception as e:
            print(e)
            return self.get_specified_compulsory_course(course_code, retry + 1)
        response_course.encoding = "gbk"
        html = Selector(response_course.text)
        course_list = html.xpath(
            '//table[@class="datelist"]//tr/td[1]/a[@href="#" and contains(@onclick, "xsxjs.aspx?xkkh=")]')
        result = []
        for course in course_list:
            onclick = course.xpath("@onclick").extract_first()
            course_name = course.xpath("text()").extract_first()
            course_key = re.search("(?<=xkkh=).+?(?=&xh)", onclick)
            course_key = course_key.group() if course_key else None
            if not course_key:
                continue
            result = self.specified_compulsory_course_search(detail_action, course_code, course_name, course_key)
        if not result:
            GUI.alert_error(
                self.GUI.text(UI.Main.Dialog.Error.TITLE),
                self.GUI.text(UI.Main.Dialog.Compulsory.NO_COURSE_PLANNING)
            )
        callback(result)
        return result

    def specified_compulsory_course_search(self, detail_action, course_code, course_name, course_key, retry=0):
        """
        具体必修课程检索
        :param detail_action:
        :param course_code:
        :param course_name:
        :param course_key:
        :param retry:
        :return:
        """
        if retry > 5:
            print('retry')
        self.fake_ip(self.action_session)
        self.action_session.headers.update({"Referer": detail_action})

        detail_params = self.request.get_compulsory_course_detail_params(
            course_code, self.csrf_token["CompulsoryCourseList"]
        )
        try:
            self.action_session.proxies = None
            detail_response = self.action_session.post(detail_action, data=detail_params)
        except Exception as e:
            print(e)
            return self.specified_compulsory_course_search(detail_action, course_code, course_name, course_key, retry + 1)

        html_detail = Selector(detail_response.text)
        extracted = self.parse_specified_compulsory_course(html_detail, course_name, course_key)
        return extracted if extracted else []

    def update_compulsory_courses(self):
        action = self.request.get_compulsory_courses_url(self.dynamic_code, self.student_code, self.fullname)

        referer = self.request.get_main_url(self.dynamic_code, self.student_code)
        self.action_session.headers.update({'Referer': referer})
        response = self.action_session.get(action)

        response.encoding = "gbk"
        html = Selector(response.text)
        self.csrf_token.update(
            {"CompulsoryCourseList": html.xpath('//input[@name="__VIEWSTATE"]/@value').extract_first()}
        )

        options = html.xpath('//select[@name="ddlKCMC"]/option')
        group = []
        for option in options:
            course_code = option.xpath("@value").extract_first()
            course_name = option.xpath("text()").extract_first()
            course_name = course_name.split("|")[-1] if course_name else course_name
            if not course_code or not course_name:
                continue
            group.append([course_code, course_name])

        for g in group:
            self.compulsory_course_list.append((g[0], g[1]))

        sorted(self.compulsory_course_list, key=lambda course: course[1])
        self.fetch_extension_course_map()

    @staticmethod
    def parse_specified_compulsory_course(html, course_name, course_key):
        """
        解析必修课具体课程
        :param html:
        :param course_name:
        :param course_key:
        :return:
        """
        selected_title = html.xpath('//table[@id="DBGrid"]//tr[@class="datelisthead"]/td/text()').extract()
        selected_title = {selected: i + 1 for i, selected in enumerate(selected_title)}

        selected_list = html.xpath('//table[@id="DBGrid"]//tr[not(@class="datelisthead")]')
        selected_list = [{
            'CourseName': course_name,
            'CourseKey': course_key,
            'CourseTime': selected.xpath('td[{}]/text()'.format(selected_title['上课时间'])).extract_first(''),
            'CourseCode': selected.xpath('td[{}]/span/input/@value'.format(selected_title['选定'])).extract_first(''),
            'Teacher': selected.xpath('td[{}]/text()'.format(selected_title['教师姓名'])).extract_first(''),
            'Capacity': int(selected.xpath('td[{}]/text()'.format(selected_title['容量(人数)'])).extract_first(0)),
            'Selected': int(selected.xpath('td[{}]/text()'.format(selected_title['已选人数'])).extract_first(0)),
        }
            for selected in selected_list
        ]

        return selected_list

    def update_general_elective_courses(self):
        """
        更新公选课列表
        :return:
        """
        action = self.request.get_general_elective_courses_url(self.dynamic_code, self.student_code, self.fullname)
        params = Network.get_general_elective_course_params(
            view_state=self.csrf_token['GeneralElectiveCourseList'],
            work='list'
        )
        self.action_session.headers.update(
            {"Referer": self.request.get_main_url(self.dynamic_code, self.student_code)}
        )
        response = self.action_session.post(action, data=params)

        if response is None:
            print('response is None')
            time.sleep(3)
            return self.update_general_elective_courses()
        response.encoding = "gbk"
        html = Selector(response.text)
        # print(response.text)
        csrf_token = html.xpath('//form[@name="xsyxxxk_form"]/input[@name="__VIEWSTATE"]/@value').extract_first()
        if '三秒防刷' in response.text:
            self.status_bar.SetStatusText(
                self.GUI.text(Msg.Main.THREE_SECOND_LIMITED)
            )
        tr_title = html.xpath('//table[@id="kcmcGrid"]/tr[@class="datelisthead"]/td').xpath('string(.)').extract()
        course_title = {selected: i + 1 for i, selected in enumerate(tr_title)}

        tr = html.xpath('//table[@id="kcmcGrid"]/tr[not(@class="datelisthead")]')
        group = []
        for tr_item in tr:
            course_code = tr_item.xpath('td[{}]/text()'.format(course_title['课程代码'])).extract_first('')
            course_name = tr_item.xpath('td[{}]/a/text()'.format(course_title['课程名称'])).extract_first('')
            course_time = tr_item.xpath('td[{}]/@title'.format(course_title['上课时间'])).extract_first('')
            course_teacher = tr_item.xpath('td[{}]/a/text()'.format(course_title['教师姓名'])).extract_first('')
            course_remain = tr_item.xpath('td[{}]/text()'.format(course_title['余量'])).extract_first('')
            course_textbook = tr_item.xpath('td[{}]/input/@value'.format(course_title['预订教材'])).extract_first('')
            course_time_mini = re.sub("{.+?}", "", course_time)
            group.append([
                '',
                course_name,
                course_time_mini,
                course_teacher,
                course_remain,
                course_code,
                'kcmcGrid:_ctl2:',
                course_time,
                course_textbook,
                'GENERAL_ELECTIVE'
            ])
            sorted(group, key=lambda course: course[1])

        if group:
            self.value_map['SelectedCourse'] = self.parse_selected_course(response)
            CheckListUtils.insert(
                self.ctrl_ref['SelectedCourseList'],
                self.value_map['SelectedCourse'],
                ['No', 'DropEvent', 'CourseName', 'CourseTime', 'Textbook']
            )
            ConfigIO.update("Cache", "Courses", value=RSAUtils.encrypt(Cache.save(group), local=True))
            return group
        else:
            self.csrf_token['GeneralElectiveCourseList'] = csrf_token
            time.sleep(3)
            return self.update_general_elective_courses()

    def get_general_elective_courses(self, callback, update=False):
        """获取公选课接口"""
        course_data = UserConfig.COURSE_DATA
        decoded_course_data = Cache.open(RSAUtils.decrypt(course_data, decode=False, local=True))
        if decoded_course_data and not update:
            callback(decoded_course_data)
        else:
            if not self.agreement_status:
                GUI.alert_error(
                    self.GUI.text(UI.Main.Dialog.Error.TITLE),
                    self.GUI.text(Msg.Main.NOT_INITIALIZED_YET)
                )
                return
            if not self.login_validate():
                self.GUI.text([Msg.Login.LOGIN_CERTIFICATE_EXPIRED, Msg.Common.RETRYING])
                self.task_running = True
                self.login_base(self.get_general_elective_courses, callback=callback)
                self.task_running = False
            course_data = self.update_general_elective_courses()
            callback(course_data)

    def send_select_record(self):
        pass

    def send_heartbeat(self, course_code, times=0):
        """服务端：心跳包"""
        GoogleRPC.heartbeat(stu_code=self.student_code, course=course_code)


    def compulsory_csrf_auth(self):
        base_action = self.request.get_compulsory_course_select_url(
            self.dynamic_code, self.value_ref['ExpectedCourseCode'][0], self.student_code
        )

        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.CSRF_AUTHENTICATING)
        )
        self.action_session.headers.update({"Referer": base_action})
        response = self.action_session.get(base_action)
        response.encoding = "gbk"
        html = Selector(response.text)
        self.compulsory_csrf_update(html)

    def general_elective_csrf_auth(self):
        base_action = self.request.get_general_elective_courses_url(self.dynamic_code, self.student_code, self.fullname)
        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.CSRF_AUTHENTICATING)
        )
        params = Network.get_general_elective_course_params(
            view_state=self.csrf_token['GeneralElectiveCourseList'],
            course_name=self.value_ref['ExpectedCourseName'][0],
            course_time=self.value_ref['ExpectedCourseTime'][0],
            work='before_pick'
        )
        params.update({
            self.value_ref['ExpectedCourseTextBookCode'][0]: self.value_ref['ExpectedCourseTextBookName'][0].encode("gbk"),
            "__EVENTARGUMENT": "ddl_sksj",
        })
        self.action_session.headers.update({"Referer": base_action})
        response = self.action_session.post(base_action, data=params)

        response.encoding = "gbk"
        html = Selector(response.text)
        self.general_elective_csrf_update(html)

        return response

    def async_func(self, func, *args):
        _loop = asyncio.get_event_loop()
        return _loop.run_in_executor(self.executor, func, *args)

    async def async_tasks(self, action, params, course_type):
        concurrent_num = 5
        if self.tasks_status and course_type == ['GENERAL_ELECTIVE']:
            await asyncio.gather(*[
                self.async_func(self.async_general_elective_submit, action, params) for _ in range(concurrent_num)
            ])
        elif self.tasks_status and course_type == ['COMPULSORY']:
            await asyncio.gather(*[
                self.async_func(self.async_compulsory_submit, action, params) for _ in range(concurrent_num)
            ])
        else:
            await asyncio.sleep(0.01)

    def start_work(self):
        """触发选课操作"""
        self.send_heartbeat(course_code=self.value_ref['ExpectedCourseCode'][0])
        self.ctrl_ref['LaunchButton'].Disable()

        if self.value_ref['ExpectedCourseType'] == ['COMPULSORY']:
            self.compulsory_csrf_auth()
            action = self.request.get_compulsory_course_select_url(
                self.dynamic_code, self.value_ref['ExpectedCourseCode'][0], self.student_code
            )
            params = Network.get_compulsory_course_select_params(
                view_state=self.csrf_token['CompulsoryCoursePost'],
                course_key=self.value_ref['ExpectedCourseKey'][0],
                textbook=self.has_textbook
            )

        elif self.value_ref['ExpectedCourseType'] == ['GENERAL_ELECTIVE']:
            self.general_elective_csrf_auth()
            action = self.request.get_general_elective_courses_url(self.dynamic_code, self.student_code, self.fullname)
            params = Network.get_general_elective_course_params(
                view_state=self.csrf_token['GeneralElectiveCoursePost'],
                course_name=self.value_ref['ExpectedCourseName'][0],
                course_time=self.value_ref['ExpectedCourseTime'][0],
                work='pick'
            )
            params.update({
                self.value_ref['ExpectedCourseTextBookCode'][0]: self.value_ref['ExpectedCourseTextBookName'][0].encode(
                    "gbk"),
                self.value_ref['ExpectedCourseCode'][0]: "on",
                "Button1": "  提交  ".encode("gbk")
            })
            if self.has_textbook:
                params.update({
                    self.value_ref['ExpectedCourseTextBook'][0]: "on"
                })
        else:

            return
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.async_tasks(action, params, self.value_ref['ExpectedCourseType']))
        self.send_heartbeat(course_code=self.value_ref["ExpectedCourseCode"])
        while True:
            if not self.login_status and not self.task_running:
                self.ctrl_ref['LaunchButton'].Disable()
                break

        self.ctrl_ref['LaunchButton'].Enable()

    def general_elective_csrf_update(self, html):
        csrf_token = html.xpath('//form[@name="xsyxxxk_form"]/input[@name="__VIEWSTATE"]/@value').extract_first()
        self.csrf_token.update({"GeneralElectiveCoursePost": csrf_token})
        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.CSRF_AUTHENTICATION_SUCCESS)
        )

    def compulsory_csrf_update(self, html):
        csrf_token = html.xpath('//form[@name="xsxjs_form"]/input[@name="__VIEWSTATE"]/@value').extract_first()
        self.csrf_token.update({"CompulsoryCoursePost": csrf_token})
        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.CSRF_AUTHENTICATION_SUCCESS)
        )

    def drop_course(self, drop_item):
        """触发退课操作"""
        self.general_elective_csrf_auth()

        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.CSRF_AUTHENTICATION_SUCCESS)
        )
        action = self.request.get_general_elective_courses_url(self.dynamic_code, self.student_code, self.fullname)
        params = Network.get_general_elective_course_params(view_state=self.csrf_token['GeneralElectiveCoursePost'],
                                                            work='drop')
        params.update({'__EVENTTARGET': drop_item})

        headers = self.request.get_headers(action)
        headers.update(self.action_session.headers)
        try:
            response = self.action_session.post(action, headers=headers, data=params)
            html = Selector(response.text)
            response.encoding = "gbk"
            self.general_elective_csrf_update(html)
        except requests.exceptions.ConnectionError:
            return False

        if not response:
            return False

        if '退选成功' in response.text:
            self.value_map['SelectedCourse'] = self.parse_selected_course(response)
            CheckListUtils.insert(
                self.ctrl_ref['SelectedCourseList'],
                self.value_map['SelectedCourse'],
                ['No', 'DropEvent', 'CourseName', 'CourseTime', 'Textbook']
            )
            return True
        else:
            return False

    @staticmethod
    def parse_selected_course(response):
        """解析已选课程列表"""

        def parse_js(code):
            drop_id = re.search("(?<=javascript:__doPostBack\(').*?(?=')", code)
            drop_id = drop_id.group() if drop_id else ''
            drop_id = drop_id.replace('$', ':')
            return drop_id

        response.encoding = "gbk"
        h = Selector(response.text)
        selected_title = h.xpath('//table[@id="DataGrid2"]//tr[@class="datelisthead"]/td/text()').extract()
        selected_title = {selected: i + 1 for i, selected in enumerate(selected_title)}
        selected_list = h.xpath('//table[@id="DataGrid2"]//tr[not(@class="datelisthead")]')
        selected_list = [{
            'No': '',
            'CourseName': selected.xpath('td[{}]/text()'.format(selected_title['课程名称'])).extract_first(''),
            'CourseTime': selected.xpath('td[{}]/text()'.format(selected_title['上课时间'])).extract_first(''),
            'Textbook': selected.xpath('td[{}]/a/text()'.format(selected_title['教材'])).extract_first(''),
            'DropEvent': parse_js(selected.xpath('td[{}]/a/@href'.format(selected_title['退选'])).extract_first(''))}
            for selected in selected_list
        ]
        return selected_list

    def parse_result(self, response):
        """解析选课请求"""
        message = ''
        response.encoding = "gbk"
        h = Selector(response.text)
        title = h.xpath('//title/text()').extract_first()
        self.value_map['SelectedCourse'] = self.parse_selected_course(response)
        for expected in self.value_ref['ExpectedCourseName']:
            for reality in self.value_map['SelectedCourse']:
                if reality['CourseName'] in expected:
                    message = self.GUI.text(Msg.Main.TASK_SELECTED)
                    self.status_bar.SetStatusText(
                        self.GUI.text(Msg.Main.TASK_SELECTED)
                    )

        if '请登录' in title or response.status_code == 302:
            message = Msg.Login.LOGIN_CERTIFICATE_EXPIRED
            self.login_status = False
            self.tasks_status = False
            self.csrf_token['GeneralElectiveCoursePost'] = None
            self.status_bar.SetStatusText(
                message
            )
        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.TASK_RUNNING, self.logger_count + 1)
        )
        self.logger_count += 1
        if response.status_code != 200:
            message = str(response.status_code)
        if '人数超过限制' in response.text:
            message = self.GUI.text(Msg.Main.NUMBER_EXCEEDS_THE_LIMIT)
        if '现在不是选课时间' in response.text:
            message = self.GUI.text(Msg.Main.NOT_START_TIME)
        if '上课时间冲突' in response.text:
            self.tasks_status = False
            self.status_bar.SetStatusText(
                self.GUI.text(Msg.Main.TIME_CONFLICT)
            )
            message = self.GUI.text(Msg.Main.TIME_CONFLICT)
        Logger.insert(
            self.ctrl_ref['LoggerList'],
            self.logger_count,
            message
        )
        CheckListUtils.insert(
            self.ctrl_ref['SelectedCourseList'],
            self.value_map['SelectedCourse'],
            ['No', 'DropEvent', 'CourseName', 'CourseTime', 'Textbook']
        )

    @staticmethod
    def fake_ip(sess: Session):
        random_ip = socket.inet_ntoa(struct.pack('>I', random.randint(0xC0A80001, 0xC0A8FEFE)))
        sess.headers.update({
            'X-Remote-Addr': random_ip,
            'Proxy-Client-IP': random_ip,
            'X-Forwarded-For': random_ip,
            'X-Remote-IP': random_ip,
            'X-Client-IP': random_ip,
            'X-Real-IP': random_ip,
        })

    def async_compulsory_submit(self, url, data: dict):
        while True:
            self.task_running = True
            if not self.tasks_status:
                break
            if self.disabled:
                self.status_bar.SetStatusText(
                    self.GUI.text([Msg.Main.HEARTBEAT_FAILED, Msg.Main.TASK_INTERRUPTED, Msg.Main.CONTACT_ADMIN])
                )
                break
            try:
                self.action_session.headers.update({"Referer": url})
                data.update({"__VIEWSTATE": self.csrf_token["CompulsoryCoursePost"]})
                response = self.action_session.post(url, data=data)
                response.encoding = 'gbk'
                html = Selector(response.text)
                self.compulsory_csrf_update(html)

            except requests.exceptions.ConnectionError:
                self.status_bar.SetStatusText(
                    self.GUI.text([Msg.Main.REQUEST_TIMEOUT, Msg.Common.RETRYING])
                )
                time.sleep(3)
                continue

            if response is None:
                self.status_bar.SetStatusText(
                    self.GUI.text([Msg.Main.REQUEST_TIMEOUT, Msg.Common.RETRYING])
                )
                time.sleep(10)
                continue
            if response.status_code == 200:
                self.parse_result(response)
            elif response.status_code == 503:
                time.sleep(3)
            elif response.status_code == 302:
                break
            else:
                time.sleep(30)
                continue
        self.task_running = False

    def async_general_elective_submit(self, url, data: dict):
        while True:
            self.task_running = True
            if not self.tasks_status:
                break
            if self.disabled:
                self.status_bar.SetStatusText(
                    self.GUI.text([Msg.Main.HEARTBEAT_FAILED, Msg.Main.TASK_INTERRUPTED, Msg.Main.CONTACT_ADMIN])
                )
                break
            try:
                self.action_session.headers.update({"Referer": url})
                data.update({"__VIEWSTATE": self.csrf_token["GeneralElectiveCoursePost"]})
                response = self.action_session.post(url, data=data)
                response.encoding = 'gbk'
                html = Selector(response.text)
                self.general_elective_csrf_update(html)

            except requests.exceptions.ConnectionError:
                self.status_bar.SetStatusText(
                    self.GUI.text([Msg.Main.REQUEST_TIMEOUT, Msg.Common.RETRYING])
                )
                time.sleep(3)
                continue

            if response is None:
                self.status_bar.SetStatusText(
                    self.GUI.text([Msg.Main.REQUEST_TIMEOUT, Msg.Common.RETRYING])
                )
                time.sleep(10)
                continue
            if response.status_code == 200:
                self.parse_result(response)
            elif response.status_code == 503:
                time.sleep(3)
            elif response.status_code == 302:
                break
            else:
                time.sleep(30)
                continue
        self.task_running = False

    def kill_thread(self):
        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Main.KILLING_WORK)
        )
        self.tasks_status = False

    def logout(self):
        self.agreement_status = False
        self.login_status = False
        url = self.request.get_logout_url(self.dynamic_code)
        headers = Network.get_headers(self.request.get_main_url(self.dynamic_code, self.student_code))
        response = self.action_session.get(url, headers=headers)
        if response is None:
            self.status_bar.SetStatusText(
                self.GUI.text(Msg.Main.REQUEST_TIMEOUT)
            )
            return
        status_code = response.status_code
        self.status_bar.SetStatusText(
            self.GUI.text(Msg.Login.LOGOUT_SUCCESS)
            if status_code == 200 else self.GUI.text(Msg.Common.ERROR_CODE, status_code)
        )
