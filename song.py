# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def _get(song_url):
	response = requests.get(song_url)
	if response.status_code == 200:
		response.encoding = "utf-8"
		soup = BeautifulSoup(response.text)
		param_tag = soup.find('param', attrs={"name": "movie"})
		player_url = param_tag["value"]
		query = urlparse(player_url).query
		return query.split("=")[1].split(",,,")


def _get_download_url(music_id, inner_url):
	def get_server_urls():
		urls = {}
		for index in range(1, 20, 1):
			url = "http://a64-%d.jyw8.com:8080/" % index
			urls[index] = url
		return urls

	download_url = inner_url
	server_urls = get_server_urls()

	if 97160 < music_id <= 105558:
		download_url = server_urls[2] + download_url
	elif 105558 < music_id <= 113933:
		download_url = server_urls[3] + download_url
	elif 113933 < music_id <= 123781:
		download_url = server_urls[4] + download_url
	elif 123781 < music_id <= 129389:
		download_url = server_urls[5] + download_url
	elif 129389 < music_id <= 138471:
		download_url = server_urls[6] + download_url
	elif 138471 < music_id <= 144784:
		download_url = server_urls[7] + download_url
	elif 144784 < music_id <= 151966:
		download_url = server_urls[8] + download_url
	elif 151966 < music_id <= 160431:
		download_url = server_urls[9] + download_url
	elif 160431 < music_id <= 167639:
		download_url = server_urls[10] + download_url
	elif 167639 < music_id <= 182926:
		download_url = server_urls[11] + download_url;
	elif 182926 < music_id <= 198890:
		download_url = server_urls[12] + download_url
	elif 198890 < music_id <= 213214:
		download_url = server_urls[13] + download_url
	elif 213214 < music_id <= 227251:
		download_url = server_urls[14] + download_url
	elif 227251 < music_id <= 240890:
		download_url = server_urls[15] + download_url
	elif 240890 < music_id <= 268960:
		download_url = server_urls[16] + download_url
	elif music_id > 268960:
		download_url = server_urls[17] + download_url
	else:
		download_url = server_urls[1] + download_url
	return download_url


class Song(object):
	def __init__(self, song_url):
		self._song_url = song_url
		self._song_info = _get(self._song_url)

	@property
	def song_url(self):
		return self._song_url

	@property
	def music_id(self):
		return int(self._song_info[0])

	@property
	def name(self):
		return self._song_info[1]

	@property
	def duration(self):
		return self._song_info[5]

	@property
	def download_url(self):
		inner_url = self._song_info[2]
		if self.music_id > 97160:
			inner_url = inner_url[6:]
		else:
			inner_url = inner_url[12:]

		if self.music_id >= 263755:
			pass
		return _get_download_url(self.music_id, inner_url)
		




