import os
import subprocess
import sys

import requests


class Updater:
    url = "https://newitd-xuanke.oss-cn-hangzhou.aliyuncs.com/main.exe"
    file_name = 'main.exe'
    tmp_file_name = 'tmp.exe'
    bat_name = 'update.bat'

    @classmethod
    def check_update(cls):
        print('正在检查更新')
        res = requests.head(cls.url)
        local_size = cls.get_size()
        server_size = int(res.headers['content-length'])
        if local_size != server_size:
            print('检测到更新，正在下载')
            cls.update()
            return False
        else:
            print('当前已经是最新版本')
            return True

    @classmethod
    def get_size(cls):
        return os.path.getsize(cls.file_name)

    @classmethod
    def update(cls):
        url = cls.url
        res = requests.get(url)
        with open(cls.tmp_file_name, "wb") as f:
            f.write(res.content)

        print('下载完成，正在安装')

        with open(cls.bat_name, 'w') as f:
            f.write("""
            @echo off
            ping -n 3 127.0.0.1 > nul
            del {}
            if not errorlevel 0 goto myfail
            ren {} {}
            if not errorlevel 0 goto myfail
            start {}
            del %0
            :myfail
            echo 更新失败：程序正在运行，请关闭所有程序后再重新打开进行更新
            pause
            """.format(cls.file_name, cls.tmp_file_name, cls.file_name, cls.file_name))
        subprocess.Popen(cls.bat_name)

        sys.exit()
