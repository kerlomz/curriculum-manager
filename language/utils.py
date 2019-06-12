#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>

from language.lang import *

__LANGUAGE_MAP = {
    0x0804: Chinese(),
    0x0409: English(),
}


def get_class(lang_id):
    return __LANGUAGE_MAP.get(lang_id)
