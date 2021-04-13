import re
from datetime import datetime

from .analyzer	import Analyzer
from ..downloader.reddit import download_rss_reddit

class Reddit_Analyzer(Analyzer):
	SITE='[reddit]'
	URL_MATCH=r'(?:https://|)(?:www\.|)reddit\.com/(?P<ID>(?:r|user)/[A-z0-9_]*)'
	TEST=[
		'https://reddit.com/r/france',
		'www.reddit.com/r/france',
		'www.reddit.com/user/reddit',
		'/user/reddit',
		'/r/seddit',
	]

	def __init__(self, url_id=''):
		self.id     = self.extract_id(url_id)
		self.content = {}

	def add_sub(self, sub):
		""" This function return the informations wich are write in sub.swy ."""
		sid = self.extract_id(sub)
		data = download_rss_reddit(sid)
		if data is None:
			return None
		return sid + '\t' + data['title']

	def write(self):
		self.file.add(
			url=self.content['url'],
			title=self.content['title'],
			url_uploader=self.content['url_sub'],
			image=self.content['image'],
			uploader=self.content['sub'],
			date=self.content['date'],
		)

	def real_analyzer(self):
		""" The main function  wich retrieve the informations and and write it
		in a file"""
		data = download_rss_reddit(self.id)
		if data is None:
			return
		for item in data['items']:
			self.content = self.info(item, {
				'url':     {'re':'<link href="(.+?)"'},
				'sub':     {'default': self.id},
				'url_sub': {'default':'https://www.reddit.com/' + self.id},
				'title':   {'re':'<title>(.+?)</title>'},
				'image':   {'re':'img src=&quot;(.+?)&quot;', 'default': self.NO_IMG},
				'date':    {'re':'<updated>(.+?)\+00:00</updated>', 'date':'%Y-%m-%dT%H:%M:%S'},
			})
			if self.content is not None:
				self.write()

	def old(self, url, lcl):
		""" The function wich is call with the option -o
		This function print the old channel or the dead channel."""
		pass

	def dead(self, url):
		""" The function wich is call with the option -d
		This function print the dead channel."""
		pass
