#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>


class Language(object):

    def __init__(self):
        self.text = None

    def find_by_id(self, _id, *params):
        if len(params) > 0:
            text = self.text.get(_id)
            for i, param in enumerate(params):
                text = text.replace('*{}'.format(i+1), str(param))
            return text
        return self.text.get(_id)
