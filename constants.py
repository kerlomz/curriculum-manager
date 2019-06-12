#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import socket
import uuid


class Variable:
    import os
    import sys
    EXEC_PATH = os.path.realpath(sys.argv[0])
    MAC_ADDRESS = ":".join([(uuid.UUID(int=uuid.getnode()).hex[-12:])[e:e + 2] for e in range(0, 11, 2)]).upper()
    HOST_NAME = socket.gethostname()


class Security:

    def __init__(self):

        self.__PUBLIC_KEY__ = [
            b'-----BEGIN RSA PUBLIC KEY-----',
            b'MIGJAoGBAJI8/9TM1+MoYriKlEsj4f65XxgNsbeXdq7uwcN8kC5QbKO89Hu5oXeq',
            b'G6GQUzJq19idmX5ybyBuBL/UWVZq6EDjKtACJfs3562czPgbtZyr3fFl2//kzjn1',
            b'Np2c7TIFDlu+xokK9+Yw/QsyGLk5grD16hccc7syRXXJ85q7DtTJAgMBAAE=',
            b'-----END RSA PUBLIC KEY-----',
            b''
        ]

        self.__PRIVATE_KEY__ = [
            b'-----BEGIN RSA PRIVATE KEY-----',
            b'MIICYgIBAAKBgQC0rpSD1/0vQVz+r/t3xTXyCsJMbiyZ9vLLc6qlPiVtdCBd3fgM',
            b'4NOTDoBinLhlVF7tBa8HyTTBMoPaB9TliKHde1ng49OhgGgi5tmUbO8WuEwmHKNh',
            b'dYy1cf+vx0dzCNYAbm6dDsspKgLxP05gIteR5LejRvAW7ZeMmO2Jfoj5zQIDAQAB',
            b'AoGAdwdDo4+YpZbj0ozQlth+b1OTKJK0I0HCNTGfy3gjY/XKlMvz61f5SbmV7mDc',
            b'QTTRzEegRPrSHCxRHENn8eFzsGIQJp3fZGRMGxLJIfzK2hFFeb2LmY5jyYmdzHn0',
            b'04PG9z6rIMmwBXKN25GaGY+F2ZV59hANahQEDkYTwE655kECRQDixi7Yhrh/T5lT',
            b'XnAhH2XnAhh87Rvox7wIg7JPPSFPDwAFEF+v2k5hORSCFi2klfnTPtSQiRbFAf7t',
            b'5M0cLdvXKSuvdQI9AMv3tMq+swqUFkRQpZAExSQeRDrEDNxBJxTp1YjbLUJCqSeL',
            b'ImBefRwtfMJO1jGZG4ufcyEphj/xw6zt+QJFAJekTs8bx2PapnzJOdHsXQgMrrNb',
            b'Gr6eUW6gIiw6hHuJXEoGmPXO1XrN4Jjcm8jjQRuxeBLumPtESmRqC348bDWEomHB',
            b'Aj0AjntiUwL2JVyfVWeU0E9Uu89c0ERly3LD70sNvMWHDzNr4NDD2dgHw6hO75mM',
            b'7SbMZDOlhDPysTac/29ZAkUAvYTJOVVofMfWwsPqU9LfsdiSL7iEeXwhZ9XcKAc2',
            b'MWtuQpVQzmLe+dipQAmVRBe43+ZFkLEWC04GKk2TxsrKVPOLOrk=',
            b'-----END RSA PRIVATE KEY-----',
            b''
        ]

        self.__LOCAL_PUBLIC_KEY__ = [
            b'-----BEGIN RSA PUBLIC KEY-----',
            b'MIGJAoGBAIDJnQuwJcDpJGFo++KO12ybtvuqYN20JdGIg6O4VYev6vAYrejimTRr',
            b'QLlr87e1IlOH/6TyNdvV8INipPTmc5CJyCEC3j6UGDGkC5HIPPC/4Ta7WZAKJQ8y',
            b'kpAg2kPfkC57XDoF5jhQy9/X4TRaVLx1A5N/5qSIrMoQV7GHeo/BAgMBAAE=',
            b'-----END RSA PUBLIC KEY-----',
            b''
        ]

        self.__LOCAL_PRIVATE_KEY__ = [
            b'-----BEGIN RSA PRIVATE KEY-----',
            b'MIICYAIBAAKBgQCAyZ0LsCXA6SRhaPvijtdsm7b7qmDdtCXRiIOjuFWHr+rwGK3o',
            b'4pk0a0C5a/O3tSJTh/+k8jXb1fCDYqT05nOQicghAt4+lBgxpAuRyDzwv+E2u1mQ',
            b'CiUPMpKQINpD35Aue1w6BeY4UMvf1+E0WlS8dQOTf+akiKzKEFexh3qPwQIDAQAB',
            b'AoGAP3AQVaOM1TuCWiE2geDOqIcDWXARiuOkBVRzU4AHUXEMDvx5HdAQm0uBdFSC',
            b'lqk4oWDKQlu0v/bgJDfArSNhkan+4mcy3kL3gP0TwfJ0El3vHtvQbNQ8Dmpg//ui',
            b'UTCMUTHBKa4F2jzPhjDwDSO/A8jVkz4Dfjh2QkPDZGjSMYkCRQCjODSPOarZCKKZ',
            b'TAY8XZxK+q+PWo9uljLI8UX7I9ZIUIRy2NBetsX4mnRRMW0U1HEieV6yqSwrXDcS',
            b'LDTL/osv0I/NIwI9AMn+2HarwiN473omvp3baGufNBSeCcKO7RJTHvjEic5bkFbs',
            b'KSx+BjIOQ6RozNyPjipkOWHQaGHwwBRXywJEdBEn7yHHCIdHeVPCq3K2DeuupHZ1',
            b'wOI2QwawCSM24j2/shvUMUYwCdVsGcDYHRPlT+qXGN2Md1kgIGAnO1lLiTj6yZkC',
            b'PAhhYVuzDo/oMY9Q0jG8a52jcka0s9T1lxJejndluA3usJNaou6sn9ctzlKg4nb4',
            b'Ib7Sf6r2OY5urZlqdwJFAICQr+g57V4uFw9eSJyNMthPAgfXKrTVQjiTUv04Cvna',
            b'M4NZeQOu2bdsUPsW2xhrabu8ARx61vovrO2FTYw45u3IhCl6',
            b'-----END RSA PRIVATE KEY-----',
            b''
        ]

    @property
    def public_key(self):
        return b"\n".join(self.__PUBLIC_KEY__)

    @property
    def private_key(self):
        return b"\n".join(self.__PRIVATE_KEY__)

    @property
    def local_public_key(self):
        return b"\n".join(self.__LOCAL_PUBLIC_KEY__)

    @property
    def local_private_key(self):
        return b"\n".join(self.__LOCAL_PRIVATE_KEY__)


class ViewState:
    GeneralElectiveAgreement = 'dDw3ODg0ODk2MDt0PDtsPGk8MT47PjtsPHQ8O2w8aTwyPjs+O2w8dDxwPHA8bDxFbmFibGVkOz47bDxvPHQ+Oz4+Oz47Oz47Pj47Pj47PoPWQFIRa0d/byHzXPM5OILT0rmM'
    CompulsoryAgreement = 'dDw3ODg0ODk2MDt0PDtsPGk8MT47PjtsPHQ8O2w8aTwyPjs+O2w8dDxwPHA8bDxFbmFibGVkOz47bDxvPHQ+Oz4+Oz47Oz47Pj47Pj47Pvb4aY0uAIvgIu2q+ccFRO/4wOQN'


class StaticPath:

    class Request:
        CAPTCHA_PATH = "CheckCode.aspx"
        LOGIN_PATH = "default2.aspx"
        LOGOUT_PATH = "logout.aspx"
        MAIN_PATH = "xs_main.aspx"
        COMMON_COURSES_PATH = "xf_xsqxxxk.aspx"
        COURSE_TABLE_PATH = "xskb.aspx"
        GENERAL_ELECTIVE_AGREEMENT_PATH = "sm_qxxxk.aspx"
        COMPULSORY_AGREEMENT_PATH = "sm_xsxkb.aspx"
        COMPULSORY_APPLY_PATH = "rlymsq.aspx"
        COMPULSORY_SEARCH_PATH = "zylb.aspx"
        COMPULSORY_SELECT_PATH = "xsxjs.aspx"
        COMPULSORY_LIST_PATH = "xsxk.aspx"
        DETAIL_INFO_PATH = "xsgrxx.aspx"

    class System:
        CONFIG_PATH = 'config.yaml'

        APP_ICON_PATH = 'resource/icon.ico'
        AUTHOR_IMG_PATH = 'resource/author.png'


