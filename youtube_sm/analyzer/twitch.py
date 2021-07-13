from ..downloader.twitch import download_twitch
from .analyzer	import Analyzer
from datetime import datetime

import re

class Twitch_Analyzer(Analyzer):
	SITE='[twitch]'
	URL_MATCH=r'(?:https://|)(?:www\.|)twitch\.tv/(?P<ID>[a-zA-Z0-9]*)(?:/.*|)'
	TEST=[
		'https://www.twitch.tv/danycaligula',
		'https://www.twitch.tv/raz404',
	]

	def __init__(self, sub=''):
		self.id = self.extract_id(sub)

	def add_sub(self, sub):
		"""
		This function return the informations wich are write in sub.swy.
		"""
		id = self.extract_id(sub)
		if id is None:
			return None
		return id + '\t' + CHANNEL

	def real_analyzer(self):
		"""
		The main function wich retrieve the informations and and write it
		in a file
		"""
		data = download_twitch(self.id)
		if data is None:
			return
		data = data[1]
		for element in data['itemListElement']:
			content = {
				'url':          element['url'],
				'title':        element['name'],
				'uploader':     self.id,
				'url_uploader': 'https://www.twitch.tv/' + self.id,
				'image':        element['thumbnailUrl'][1],
				'view':         element['interactionStatistic']['userInteractionCount'],
				'date':         datetime.strptime(element['uploadDate'], '%Y-%m-%dT%H:%M:%SZ'),
			}
			print(content['url'])
			if content is not None and re.match('https://www.twitch.tv/.*', content['url']):
				self.file.add(**content)
