#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: kerlomz <kerlomz@gmail.com>
import os

from PyInstaller.__main__ import run

import config as client

if __name__ == '__main__':

    opts = ['client_release.spec', '--distpath=dist/client']
    run(opts)
    _o = 'client.exe'
    _t = 'client{}'.format(client.SystemConfig.CLIENT_VER)
    if os.path.exists('dist\\client\\{}.exe'.format(_t)):
        os.remove('dist\\client\\{}.exe'.format(_t))
    os.rename('dist\\client\\{}'.format(_o), 'dist\\client\\{}.exe'.format(_t))
