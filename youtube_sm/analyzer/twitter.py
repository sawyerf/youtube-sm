from .analyzer	import Analyzer
from ..downloader.twitter import download_twitter
from ..core.tools import log
from datetime import datetime

import re

class Twitter_Analyzer(Analyzer):
	SITE='[twitter]'
	URL_MATCH=r'(?:https://|)(?:www\.|)twitter\.com/(?P<ID>[A-Za-z0-9_-]*)'
	TEST=[
		'https://twitter.com/UsulduFutur',
		'https://twitter.com/notweet4ever',
		'https://twitter.com/NoTweet',
		'UsulduFutur',
		'notweet4ever',
		'NoTweet',
	]

	def __init__(self, sub=''):
		self.id = self.extract_id(sub)

	def add_sub(self, sub):
		uid = self.extract_id(sub)
		if download_twitter(uid) is None:
			return None
		return uid + '\t '

	def real_analyzer(self):
		data = download_twitter(self.id)
		if data is None:
			return
		for tweet in data['globalObjects']['tweets'].values():
			content = {
				'url': 'https://twitter.com/{}/status/{}'.format(self.id, tweet['id_str']),
				'url_uploader': 'https://twitter.com/{}'.format(self.id),
				'title': tweet['full_text'],
				'date': datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'),
			 	'uploader': self.id,
				'image': self.NO_IMG,
			}
			if 'card' in tweet and 'binding_values' in tweet['card']:
				for var in tweet['card']['binding_values']:
					if 'image' in var and 'original' in var:
						content['image'] = tweet['card']['binding_values'][var]['image_value']['url']
						break
			self.file.add(**content)

	def old(self, url, since):
		sub = self.extract_id(url)
		data = download_twitter(sub)
		if data is None:
			self.subis(sub, self.ISDEAD)
		elif data['globalObjects']['tweets'] == {}:
			self.subis(sub, self.ISEMPTY)
		else:
			first = list(data['globalObjects']['tweets'].values())[0]
			date = datetime.strptime(first['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
			if since > date:
				self.subis(sub, date)
			else:
				self.subis(sub, self.ISOK)

	def dead(self, url):
		sub = self.extract_id(url)
		data = download_twitter(sub)
		if data is None:
			self.subis(sub, self.ISDEAD)
		elif data['globalObjects']['tweets'] == {}:
			self.subis(sub, self.ISEMPTY)
		else:
			self.subis(sub, self.ISOK)
