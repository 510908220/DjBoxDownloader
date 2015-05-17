# -*- coding: utf-8 -*-
"""
文件下载器
1.第一阶段实现文件的下载
2.支持断点续传
"""


import sys


def progress_bar(procent):
    """
    控制台显示进度条
    :param procent: 下载完成百分比
    :return:
    """
    buffer = "%{0} {1}".format(procent, int(procent / 5) * "#")
    sys.stdout.write("\r%s" % buffer)
    sys.stdout.flush()





