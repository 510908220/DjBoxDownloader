# -*- coding: utf-8 -*-
"""
文件下载器
1.第一阶段实现文件的下载
2.支持断点续传
"""

import queue
import threading
import requests
import time
import os


def worker(download_url, progress, local_path):
    def update_progress(total_size, recived_size):
        percent = int((recived_size / total_size) * 100)
        if progress.empty():
            progress.put_nowait(percent)

    r = requests.get(download_url, stream=True)
    total_size = int(r.headers['Content-Length'])
    print("total_size is", total_size)

    with open(local_path, 'wb') as f:
        recived_size = 0
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                recived_size += len(chunk)
                update_progress(total_size, recived_size)
                f.write(chunk)
                f.flush()

def progress_bar(procent):
    os.system('clear')
    buffer = "进度:%{0} {1}".format(procent, procent * "+")
    print(buffer)

class Downloader(object):
    def __init__(self, download_url, local_path):
        self._download_url = download_url
        self._local_path = local_path
        self._progress = queue.Queue(1)
        self._last_percent = 0
        self._thread = None

    @property
    def progress(self):
        """
        :return:下载进度
        """
        percent = 0
        if self._progress.full():
            percent = self._progress.get_nowait()
            self._last_percent = percent
        else:
            percent = self._last_percent
        return percent


    @property
    def finished(self):
        return self._thread.is_alive()

    def start(self):
        self._thread = threading.Thread(target=worker, args=(self._download_url, self._progress, self._local_path))
        self._thread.daemon = True
        self._thread.start()

if __name__ == "__main__":
    url = "http://a64-5.jyw8.com:8080/up20100924-1/DJ%CE%CA%C7%E9-2010%C7%BF%BA%B4%B6%AF%B8%D0%B3%B5%D4%D8%C8%AB%D6%D0%CE%C4Club.mp3?up20100924-1/DJ%CE%CA%C7%E9-2010%C7%BF%BA%B4%B6%AF%B8%D0%B3%B5%D4%D8%C8%AB%D6%D0%CE%C4C8ub.mp3?50886618630126432167401881173198672747524287525838"
    path  = "d:\\aa.mp3"
    dw = Downloader(url, path)
    dw.start()
    while  dw.finished:
        progress_bar(dw.progress)
        time.sleep(2)





