# -*- encoding: utf-8 -*-

from urllib.parse import urljoin
import sys
import os
import requests
from bs4 import BeautifulSoup

import song
import util
import downloader
import time

MOST_DOWNLOAD_PAGE_URL = "http://www.djyule.com/downPH.htm"
BASE_URL = "http://www.djyule.com"


def _get(song_url):
	response = requests.get(song_url)
	if response.status_code == 200:
		response.encoding = "utf-8"
		return response.text


def get_page_urls():
	def get_page_count():
		html = _get(MOST_DOWNLOAD_PAGE_URL)
		if html:
			soup = BeautifulSoup(html)
			div_page = soup.find('div', attrs={"class": "List_Page3"})
			if div_page:
				a_items = div_page.find_all("a")
				if len(a_items) > 0:
					href = a_items[-1]["href"]
					return int(href.split(".")[0].split("_")[1])  # downPH_50.htm

	page_urls = []
	count = get_page_count()

	for page_index in range(1, 50 + 1):
		if page_index == 1:
			url = MOST_DOWNLOAD_PAGE_URL
		else:
			url = "http://www.djyule.com/downPH_%d.htm" % page_index
		page_urls.append(url)
	return page_urls


def get_song_urls(page_url):
	html = _get(page_url)
	song_urls = []
	if html:
		soup = BeautifulSoup(html)
		form = soup.find('form', attrs={"id": "frmList"})
		# a href="/DJ/120696.htm" target="_blankDJPlay"
		a_items = form.find_all("a", {"target": "_blankDJPlay"})
		for item in a_items:
			song_url = urljoin(BASE_URL, item["href"])
			song_urls.append(song_url)
	return song_urls


# 命令行控制下载全部，部分，等
def _get_songs():
	# if not os.path.exists(MUSIC_STORE):
	# os.makedirs(MUSIC_STORE)
	page_urls = get_page_urls()
	song_urls = get_song_urls(page_urls[0])[0:10]
	songs = []
	for song_url in song_urls:
		song_ = song.Song(song_url)
		if song_.error:
			continue
		songs.append(song_)
	return songs


def main():
	songs = _get_songs()
	dd = downloader.DownloadManager(concurrency=2, time_out=60)
	dd.add_jobs(songs)
	dd.start()
	while not dd.finished():
		dd.block_check()
		time.sleep(2)

if __name__ == "__main__":
	sys.exit(main())