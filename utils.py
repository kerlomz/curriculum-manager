#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import time
import io
import sys
import grpc
import base64
import datetime
import requests
import grpc_pb2
import grpc_pb2_grpc
from PIL import ImageGrab
from urllib import parse
from requests import Session, Request
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from language.utils import *
from config import *

security = Security()
PUBLIC_KEY = security.public_key
PRIVATE_KEY = security.private_key
LOCAL_PUBLIC_KEY = security.local_public_key
LOCAL_PRIVATE_KEY = security.local_private_key


class System(object):

    @staticmethod
    def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @staticmethod
    def test_image(h):
        """JPEG"""
        if h[:3] == b"\xff\xd8\xff":
            return 'jpeg'
        """PNG"""
        if h[:8] == b"\211PNG\r\n\032\n":
            return 'png'
        """GIF ('87 and '89 variants)"""
        if h[:6] in (b'GIF87a', b'GIF89a'):
            return 'gif'
        """TIFF (can be in Motorola or Intel byte order)"""
        if h[:2] in (b'MM', b'II'):
            return 'tiff'
        if h[:2] == b'BM':
            return 'bmp'
        """SGI image library"""
        if h[:2] == b'\001\332':
            return 'rgb'
        """PBM (portable bitmap)"""
        if len(h) >= 3 and \
                h[0] == b'P' and h[1] in b'14' and h[2] in b' \t\n\r':
            return 'pbm'
        """PGM (portable graymap)"""
        if len(h) >= 3 and \
                h[0] == b'P' and h[1] in b'25' and h[2] in b' \t\n\r':
            return 'pgm'
        """PPM (portable pixmap)"""
        if len(h) >= 3 and h[0] == b'P' and h[1] in b'36' and h[2] in b' \t\n\r':
            return 'ppm'
        """Sun raster file"""
        if h[:4] == b'\x59\xA6\x6A\x95':
            return 'rast'
        """X bitmap (X10 or X11)"""
        s = b'#define '
        if h[:len(s)] == s:
            return 'xbm'
        return None


class GUI(object):

    def __init__(self, root, lang):
        self.lang = lang
        self.root = root
        # self.menu_bar = MenuBar()

    class __Language(object):

        def __init__(self):
            self.default = 'en-US'

        def get(self, lang, _id, *params):
            lang_id = LANGUAGE_MAP.get(lang)
            if not lang_id:
                return
            _class = get_class(lang_id)
            if not _class:
                return self.get('en-US', _id, *params)
            return _class.find_by_id(_id, *params)

        def delimiter(self, lang):
            lang_id = LANGUAGE_MAP.get(lang)
            if not lang_id:
                return self.delimiter(self.default)
            return DELIMITER_MAP[lang_id]

    def text(self, _id, *params):
        _lang = self.__Language()
        if isinstance(_id, list) and len(_id) > 0:
            group = [_lang.get(self.lang, i, *params) for i in _id]
            return _lang.delimiter(self.lang).join(group)
        return _lang.get(self.lang, _id, *params)

    @staticmethod
    def alert_error(title, message):
        from wx import MessageDialog, YES_DEFAULT, ICON_ERROR
        dlg = MessageDialog(None, message=message, caption=title, style=YES_DEFAULT | ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()

    @staticmethod
    def alert_message(title, message):
        from wx import MessageDialog, YES_DEFAULT, ICON_INFORMATION
        dlg = MessageDialog(None, message=message, caption=title, style=YES_DEFAULT | ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def build_menu(self, root, data):
        from wx import MenuBar
        menu_bar = MenuBar()
        for eachMenuData in data:
            menu_label = eachMenuData[0]
            menu_items = eachMenuData[1]
            menu_bar.Append(self.__build_menu(menu_items), menu_label)
        root.SetMenuBar(menu_bar)

    def __build_menu(self, menu_data):
        from wx import Menu, NewId
        menu = Menu()
        for each_item in menu_data:
            if len(each_item) == 2:
                label = each_item[0]
                sub_menu = self.__build_menu(each_item[1])
                menu.AppendMenu(NewId(), label, sub_menu)
            else:
                self.__menu_item(menu, *each_item)
        return menu

    def __menu_item(self, menu, label, status, handler, kind=None):
        from wx import ITEM_NORMAL, EVT_MENU
        if kind is None:
            kind = ITEM_NORMAL
        if not label:
            menu.AppendSeparator()
            return
        menu_item = menu.Append(-1, label, status, kind)
        self.root.Bind(EVT_MENU, handler, menu_item)


class Network(object):

    def __init__(self):
        self.session = Session()

    @staticmethod
    def time(delay=0, str_format=True):
        localtime = time.localtime(time.time() + 60 * delay)
        try:
            r = requests.get('http://baidu.com', timeout=1)
            ts = r.headers.get('Date')
            ts = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
            localtime = time.localtime(time.mktime(ts) + (8 * 60 + delay) * 60)
        except requests.exceptions.ConnectionError:
            pass
        finally:
            return "%u-%02u-%02u %02u:%02u:%02u" % (
                localtime.tm_year, localtime.tm_mon, localtime.tm_mday, localtime.tm_hour, localtime.tm_min,
                localtime.tm_sec) if str_format else localtime

    def get_login_url(self, dynamic_code):
        return self.get_url(dynamic_code, StaticPath.Request.LOGIN_PATH)

    def get_logout_url(self, dynamic_code):
        return self.get_url(dynamic_code, StaticPath.Request.LOGOUT_PATH)

    def get_main_url(self, dynamic_code, stu_id):
        return self.get_url(dynamic_code, StaticPath.Request.MAIN_PATH, dict(xh=stu_id))

    def get_captcha_url(self, dynamic_code):
        return self.get_url(dynamic_code, StaticPath.Request.CAPTCHA_PATH)

    def get_compulsory_courses_url(self, dynamic_code, stu_id, fullname):
        try:
            from urllib.parse import quote
        except ImportError:
            from urllib import quote
        return self.get_url(
            dynamic_code,
            StaticPath.Request.COMPULSORY_APPLY_PATH,
            dict(xh=stu_id, xm=fullname.encode('gbk'), gnmkdm="N121109")
        )

    def get_compulsory_course_select_url(self, dynamic_code, course_key, stu_id):
        try:
            from urllib.parse import quote
        except ImportError:
            from urllib import quote
        return self.get_url(
            dynamic_code,
            StaticPath.Request.COMPULSORY_SELECT_PATH,
            dict(xh=stu_id, xkkh=course_key)
        )

    def get_compulsory_search_url(self, dynamic_code, stu_id):
        try:
            from urllib.parse import quote
        except ImportError:
            from urllib import quote
        return self.get_url(
            dynamic_code,
            StaticPath.Request.COMPULSORY_SEARCH_PATH,
            dict(xh=stu_id)
        )

    def get_general_elective_courses_url(self, dynamic_code, stu_id, fullname):
        try:
            from urllib.parse import quote
        except ImportError:
            from urllib import quote
        return self.get_url(
            dynamic_code,
            StaticPath.Request.COMMON_COURSES_PATH,
            dict(xh=stu_id, xm=fullname.encode('gbk'), gnmkdm="N121102")
        )

    def get_course_table_url(self, dynamic_code, stu_id, stu_year, stu_term):
        return self.get_url(
            dynamic_code,
            StaticPath.Request.COURSE_TABLE_PATH,
            dict(xh=stu_id, xhxx="{}{}{}".format(stu_id, stu_year, stu_term))
        )

    @staticmethod
    def status(url, timeout=30):
        session = Session()
        request = Request('GET', url)
        prepped = request.prepare()
        session.max_redirects = 1
        if timeout:
            request.timeout = timeout
        try:
            response = session.send(prepped)
            return response.status_code
        except requests.exceptions.ConnectionError:
            return -1

    @staticmethod
    def get_url(dynamic_code, path, param=None):
        serialized_param = "?{}".format(parse.urlencode(param)) if param else ""

        if not dynamic_code:
            return "http://{}/{}{}".format(NetworkConfig.HOST_SERVER, path, serialized_param)
        return "http://{}/({})/{}{}".format(NetworkConfig.HOST_SERVER, dynamic_code, path, serialized_param)

    @staticmethod
    def get_headers(referer):
        return {
            'origin': 'http://{}'.format(NetworkConfig.HOST_SERVER),
            'referer': referer,
        }

    @staticmethod
    def get_general_elective_course_params(view_state, course_time: str = None, course_name: str = None, work: str = 'list'):
        params = {
            "TextBox1": course_name.encode("gbk") if course_name else '',
            "__EVENTARGUMENT": "",
            "__EVENTTARGET": "",
            "__VIEWSTATE": view_state,
            "ddl_kcgs": "",
            "ddl_kcxz": "",
            "ddl_sksj": course_time.encode("gbk") if course_time else '',
            "ddl_xqbs": "1",
            "ddl_ywyl": "",
            "dpkcmcGrid:txtChoosePage": "1",
            "dpkcmcGrid:txtPageSize": "150",
        }
        return params

    @staticmethod
    def get_compulsory_course_select_params(view_state, course_key: str = None, textbook=True):
        params = {
            "__EVENTARGUMENT": "",
            "__EVENTTARGET": "Button1",
            "__VIEWSTATE": view_state,
            "xkkh": course_key,
            "RadioButtonList1": "1" if textbook else "0",
        }
        return params

    @staticmethod
    def get_compulsory_course_search_params(course_code: str):
        params = {
            "TextBox1": course_code,
            "__EVENTARGUMENT": "",
            "__EVENTTARGET": "",
            "__VIEWSTATE": "dDwxODQwNDgxNDkxO3Q8cDxsPHhuO3hxO1hZOz47bDwyMDE5LTIwMjA7MTvorqHnrpfmnLrkuI7orqHnrpfnp5HlrablrabpmaI7Pj47bDxpPDE+Oz47bDx0PDtsPGk8Mz47aTw1PjtpPDc+O2k8OT47PjtsPHQ8cDxwPGw8R3JvdXBOYW1lOz47bDxjeDs+Pjs+Ozs+O3Q8O2w8aTwwPjs+O2w8dDw7bDxpPDE+O2k8Mj47aTw0Pjs+O2w8dDx0PHA8cDxsPERhdGFUZXh0RmllbGQ7RGF0YVZhbHVlRmllbGQ7PjtsPHh5bWM7eHlkbTs+Pjs+O3Q8aTw5PjtAPOiuoeeul+acuuS4juiuoeeul+enkeWtpuWtpumZojvllYblrabpmaI75L+h5oGv5LiO55S15rCU5bel56iL5a2m6ZmiO+W3peeoi+WtpumZojvljLvlrabpmaI75Yib5oSP5LiO6Im65pyv6K6+6K6h5a2m6ZmiO+azleWtpumZojvkvKDlqpLkuI7kurrmloflrabpmaI75aSW5Zu96K+t5a2m6ZmiOz47QDwwMTswNTswMjswMzswNDsxMDswOTswNzswODs+PjtsPGk8MD47Pj47Oz47dDxwPHA8bDxUZXh0Oz47bDwzMTcwMjQxMTs+Pjs+Ozs+O3Q8dDxwPHA8bDxEYXRhVGV4dEZpZWxkO0RhdGFWYWx1ZUZpZWxkOz47bDxuajtuajs+Pjs+O3Q8aTwxOT47QDwyMDIwOzIwMTk7MjAxODsyMDE3OzIwMTY7MjAxNTsyMDE0OzIwMTM7MjAxMjsyMDExOzIwMTA7MjAwOTsyMDA4OzIwMDc7MjAwNjsyMDA1OzIwMDQ7MjAwMzsyMDAyOz47QDwyMDIwOzIwMTk7MjAxODsyMDE3OzIwMTY7MjAxNTsyMDE0OzIwMTM7MjAxMjsyMDExOzIwMTA7MjAwOTsyMDA4OzIwMDc7MjAwNjsyMDA1OzIwMDQ7MjAwMzsyMDAyOz4+O2w8aTwzPjs+Pjs7Pjs+Pjs+Pjt0PDtsPGk8MD47PjtsPHQ8O2w8aTwwPjs+O2w8dDx0PHA8cDxsPERhdGFUZXh0RmllbGQ7RGF0YVZhbHVlRmllbGQ7PjtsPHp5bWM7enlkbTs+Pjs+O3Q8aTw0PjtAPOe7n+iuoeWtpjvorqHnrpfmnLrnp5HlrabkuI7mioDmnK875L+h5oGv566h55CG5LiO5L+h5oGv57O757ufMTvova/ku7blt6XnqIs7PjtAPDAxMTI7MDEyMTswMTI0OzAxMzE7Pj47Pjs7Pjs+Pjs+Pjt0PHA8bDxzdHlsZTs+O2w8ZGlzcGxheTpub25lOz4+O2w8aTw2Pjs+O2w8dDxAMDw7Ozs7Ozs7Ozs7Pjs7Pjs+Pjs+Pjs+PjtsPHp4O2Z4O2Z4O2N4O2N4Oz4+kFrE+t7lF2vKyHXnjK5EuhC0Axs=",
            "cx": "cx",
            "RadioButtonList1": "3",
            "Button3": "确  定",
        }
        return params

    @staticmethod
    def get_compulsory_course_detail_params(course_code: str, view_state):
        params = {
            "ddlKCMC": course_code,
            "__EVENTARGUMENT": "__EVENTTARGET",
            "__EVENTTARGET": "",
            "__VIEWSTATE": view_state,
            "kcmc": "",
        }
        return params

    @staticmethod
    def get_login_params(identifier, password, captcha, token):
        try:
            radio_button_text = "学生".encode("gbk")
        except UnicodeDecodeError:
            import sys
            reload(sys)
            sys.setdefaultencoding('utf8')
            radio_button_text = "学生".encode("gbk")
        return {
            "Button1": "",
            "TextBox1": "",
            "TextBox2": password,
            "txtSecretCode": captcha,
            "__VIEWSTATE": token,
            "RadioButtonList1": radio_button_text,
            "txtUserName": identifier,
            "hidPdrs": "",
            "hidsc": "",
            "lbLanguage": ""
        }


class RSAUtils(object):

    @staticmethod
    def encrypt(plain_text, local=False):
        public_key = RSA.importKey(LOCAL_PUBLIC_KEY if local else PUBLIC_KEY)
        _p = Cipher_pkcs1_v1_5.new(public_key)
        plain_text = plain_text.encode('utf-8') if isinstance(plain_text, str) else plain_text
        # 1024bit key
        try:
            default_encrypt_length = 117
            len_content = len(plain_text)
            if len_content < default_encrypt_length:
                return base64.b64encode(_p.encrypt(plain_text)).decode()
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_encrypt_length:
                    params_lst.append(_p.encrypt(plain_text[offset:offset + default_encrypt_length]))
                else:
                    params_lst.append(_p.encrypt(plain_text[offset:]))
                offset += default_encrypt_length
            target = b''.join(params_lst)
            return base64.b64encode(target).decode()
        except ValueError:
            return None

    @staticmethod
    def decrypt(cipher_text, decode=True, local=False):
        private_key = RSA.importKey(LOCAL_PRIVATE_KEY if local else PRIVATE_KEY)
        _pri = Cipher_pkcs1_v1_5.new(private_key)
        cipher_text = base64.b64decode(cipher_text if isinstance(cipher_text, bytes) else cipher_text.encode('utf-8'))
        # 1024bit key
        try:
            default_length = 128
            len_content = len(cipher_text)
            if len_content < default_length:
                return _pri.decrypt(cipher_text, "ERROR").decode()
            offset = 0
            params_lst = []
            while len_content - offset > 0:
                if len_content - offset > default_length:
                    params_lst.append(_pri.decrypt(cipher_text[offset: offset + default_length], "ERROR"))
                else:
                    params_lst.append(_pri.decrypt(cipher_text[offset:], "ERROR"))
                offset += default_length
            target = b''.join(params_lst)
            return target.decode() if decode else target
        except ValueError:
            return None


class CheckListUtils(object):

    @staticmethod
    def insert(parent, data, dict_map: list = None, clear=True, focus=False):
        if not parent:
            return None
        if parent.ItemCount > 0 and clear:
            parent.DeleteAllItems()
        if not data:
            return None
        for i, item in enumerate(data):
            parent.InsertItem(i, '')
            for ii, j in enumerate(dict_map):
                parent.SetItem(i, ii, item[j])
            parent.CheckItem(i, True)
            if focus:
                parent.Focus(i)


class Logger(object):

    @staticmethod
    def insert(parent, index, message):
        parent.InsertItem(index - 1, str(index))
        parent.SetItem(index - 1, 1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        parent.SetItem(index - 1, 2, message)
        parent.Focus(index - 1)

    @staticmethod
    def grab_screen():
        im = ImageGrab.grab()
        im = im.convert('L')
        output = io.BytesIO()
        im.save(output, format='PNG')
        data_bin = output.getvalue()
        output.close()

        return data_bin


class File(object):

    @staticmethod
    def resource_path(relative_path):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)


class ResponseParser:

    def __init__(self, host: str, port):
        self._url = '{}:{}'.format(host, port)

    def request(self, key, encrypted=True) -> object:
        channel = grpc.insecure_channel(self._url)
        stub = grpc_pb2_grpc.VerificationStub(channel)
        response = stub.verification(grpc_pb2.VerificationRequest(
            key=self.dumps(key) if encrypted else key
        ))
        return self.parse(response.result)

    @staticmethod
    def dumps_response(key) -> grpc_pb2.VerificationResult:
        return grpc_pb2.VerificationResult(result=ResponseParser.dumps(key))

    @staticmethod
    def parse(request):
        decrypted_object = RSAUtils.decrypt(request, decode=False)
        return Cache.open(decrypted_object)

    @staticmethod
    def dumps(response):
        return RSAUtils.encrypt(Cache.save(response))


if __name__ == '__main__':
    # r = RSAUtils.decrypt("DlzlbKhV2KP7WM3k4O/cye4JRtDgpEf4b7HITMHbQTr2szm7egctEe7U+69xDcunwo5IyyJQwwuDBmve1dwtpXceNhgwOSn9lv6HLMGw9J+Qx68I0OexR3FWQFSpogvOiGwo4imEeAXmpqYtkj5Q1sJ1TfYt0ZcYAo7XJcd5NPM=")
    # print(r)
    # t = ResponseParser.dumps([222])
    # print(t)
    import core
    c = core.Core()
    o = ResponseParser("localhost", port=5449)
    import entity
    d = entity.Device().from_core(c)
    ll = c.machine_code_auth(stu_code="31301188", c_volume_serial_number=d.c_volume_serial_number, mac_addr=d.mac_addr, hostname=d.hostname)
    print(ll)
    d.add_license("31301188", "90909090")
    oo = entity.ClientMessage(device=d, stu_code="31301188")
    print(oo.context)
    r = ResponseParser("localhost", port=5449).request(entity.ClientMessage(device=entity.Device().from_core(c), stu_code="31301188").send(body={"123": 123}))
    # print(r)
    print(type(r))
    yy = r.context.body
    print(yy)