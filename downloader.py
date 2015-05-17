# -*- coding: utf-8 -*-
"""
1.采用多进程实现下载，这样可以在下载部分出现阻塞时将进程结束掉（线程无法直接结束掉）
2.下载管理部分可以看做一个简单的进程池，加入了进程超时检测。
"""

import requests
import time
from multiprocessing import (Process, Value, cpu_count, JoinableQueue, Queue)


class DownloadProcess(Process):
	def __init__(self, jobs, results):
		Process.__init__(self)
		self.jobs_ = jobs
		self.results_ = results
		self.task_start_time_ = Value('d', 0.0)
		self.task_start_time_.value = time.time()
		self.current_song = None
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
				self.current_song = song
				self._download(song.download_url, song.save_path)
			except Exception:
				pass
			finally:
				self.results_.put(1)
				self.jobs_.task_done()


class DownloadManager(object):
	def __init__(self, concurrency=cpu_count(), time_out=10 * 60):
		self.concurrency_ = concurrency
		self.jobs_ = None
		self.results_ = None
		self.processes_ = []
		self.time_out_ = time_out
		self.start_flag_ = False
		self.job_count_ = 0
		self.time_out_count_ = 0

	def _create_processes(self):
		for _ in range(self.concurrency_):
			process = DownloadProcess(self.jobs_, self.results_)
			process.daemon = True  # 守护进程
			self.processes_.append(process)

	def add_jobs(self, songs):
		self.time_out_count_ = 0
		self.jobs_ = JoinableQueue()
		self.results_ = Queue()

		for song in songs:
			self.jobs_.put(song)
			self.job_count_ += 1

	def block_check(self):
		def check(current_time, process):
			interval = current_time - process.task_start_time
			if interval > self.time_out_:
				return True
			return False

		current_time = time.time()

		time_out_indexs = []
		for index, process in enumerate(self.processes_):
			if check(current_time, process):
				print("歌曲:", process.current_song,"下载超时...")
				process.terminate()
				while process.is_alive():
					time.sleep(0.01)
					process.terminate()
				time_out_indexs.append(index)

		for time_out_index in time_out_indexs:
			self.time_out_count_ += 1
			process = DownloadProcess(self.jobs_, self.results_)
			process.daemon = True
			self.processes_[time_out_index] = process
			process.start()

	def start(self):
		if self.start_flag_:
			return
		if not self.processes_:
			self._create_processes()
		for p in self.processes_:
			p.start()
		self.start_flag_ = True

	def progress(self):
		progress_info = "歌曲数:{0} 已下载{1}, 超时数: {2}".format()
		return progress_info
	
	def finished(self):
		if self.results_.qsize() + self.time_out_count_ == self.job_count_:
			return True
		return False









