# -*- coding: utf-8 -*-
"""
1.采用多进程实现下载，这样可以在下载部分出现阻塞时将进程结束掉（线程无法直接结束掉）
2.下载管理部分可以看做一个简单的进程池，加入了进程超时检测。
"""

import requests
import time
from multiprocessing import (Process, Value, cpu_count, JoinableQueue, Queue)


class DownloadProcess(Process):
    def __init__(self, jobs):
        Process.__init__(self)
        self.jobs_ = jobs
        self.task_start_time_ = Value('d', 0.0)

    @property
    def task_start_time(self):
        return self.task_start_time_.value

    def _download(self, download_url, save_path):
        try:
            self.task_start_time_.value = time.time()
            r = requests.get(download_url, stream=True)
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        f.flush()
            self.task_start_time_.value = 0.0
        except Exception:
            self.task_start_time_.value = 0.0
            pass

    def run(self):
        while True:
            try:
                song = self.jobs_.get()
                self._download(song.download_url, song.save_path)
            except Exception:
                pass
            finally:
                self.jobs_.task_done()


class DownloadManager(object):
    def __init__(self, concurrency=cpu_count(), time_out=10 * 60):
        self.concurrency_ = concurrency
        self.jobs_ = JoinableQueue()
        self.processes_ = []
        self.time_out_ = time_out

    def _create_processes(self):
        for _ in range(self.concurrency_):
            process = DownloadProcess(self.jobs_)
            process.daemon = True  # 守护进程
            self.processes_.append(process)

    def add_jobs(self, songs):
        for song in songs:
            self.jobs_.put(song)

    def block_check(self):
        def check(current_time, process):
            interval = current_time - process.task_start_time
            if interval > self.time_out:
                return True
            return False

        current_time = time.time()
        for process in self.processes_:
            if check(current_time, process):
                process.terminate()
                while process.is_alive():
                    time.sleep(0.01)
                    process.terminate()
                process = DownloadProcess(self.jobs_)
                process.daemon = True

    def start(self):
        for p in self.processes_:
            p.start()

    def finished(self):
        return self.jobs_.empty()









