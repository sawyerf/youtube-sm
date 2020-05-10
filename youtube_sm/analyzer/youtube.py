import re

from datetime     import datetime, timedelta
from ..core.tools import log
from .analyzer    import Analyzer
from ..downloader.youtube import (
	download_xml,
	download_html,
)


class Youtube_Analyzer(Analyzer):
	SITE='[youtube]'
	URL_MATCH=r'(?:https://|)(?:www\.|)youtube\.com/(?P<type>channel/|user/|playlist\?list=)(?P<ID>[a-zA-Z0-9_-]*)'
	RE_CHANNEL=r'UC[A-Za-z0-9_-]{22}$'
	RE_PLAYLIST=r'PL[A-Za-z0-9_-]{32}$'
	TEST=[
		'https://www.youtube.com/channel/UCyg3MF1KU3dUK0HJBBoRYOw',
		'https://www.youtube.com/playlist?list=PL0H7ONNEUnnt59niYAZ07dFTi99u2L2n_',
		'https://www.youtube.com/channel/UCDlLfadiQHJuFkJnSBBnQsQ',
		'UCyg3MF1KU3dUK0HJBBoRYOw',
		'PL0H7ONNEUnnt59niYAZ07dFTi99u2L2n_',
		'UCDlLfadiQHJuFkJnSBBnQsQ',
	]

	def __init__(self, url_id=''):
		self.id = self.extract_id(url_id)
		self.type = self._type_id(self.id)  # True --> chanel False -- > Playlist
		self.content = None

	def add_sub(self, url):
		sub = self.extract_id(url)
		tid = self._type_id(sub)
		data = download_xml(sub, type_id=tid, split=False)
		if data is None:
			log.Error("The channel/playlist can't be add. It could be delete.")
			return None
		match = re.findall(r'<(?:title|name)>(.+?)</(?:title|name)>', data)
		if match != []:
			return sub + '\t' + match[0]
		log.Warning("The channel/playlist can't be add. It could be delete.")
		return None

	def real_analyzer(self):
		"""Recover all the videos of a channel or a playlist
		and add the informations in $HOME/.cache/youtube_sm/data/."""
		if self.method == '0':
			linfo = download_xml(self.id, self.type)
		elif self.method == '1':
			linfo = download_html(self.id, self.type)
		if linfo is None:
			return
		info = self.info_rss
		if self.method == '1':
			info = self.info_html
			if self.type:  # Channel
				self.channel = re.findall('<title>(.*)', linfo[0])
				del linfo[0]
		for i in linfo:
			info(i)
			if self.content is not None:
				self.write()

	def _full_url(self):
		if self.type:
			return 'https://www.youtube.com/channel/' + self.id
		return 'https://www.youtube.com/playlist?list=' + self.id

	def info_html(self, i):
		"""Recover the informations of the html page"""
		if self.type:  # Channel
			self.content = self.info(i, {
				'url': {'re': r'href="/watch\?v=(.{11})"'},
				'title': {'re': r'dir="ltr" title="(.+?)"'},
				'date': {'re': r'</li><li>(.+?)</li>', 'func': self.date_convert},
				'uploader': {'default': self.channel},
				'view': {'re': r'class="yt-lockup-meta-info"><li>(.+?)\ views'},
			})
		else:  # Playlist
			self.content = self.info(i, {
				'url': {'re':r'data-video-id="(.{11})"'},
				'title': {'re':r'data-video-title="(.+?)"'},
				'uploader': {'re':r'data-video-username="(.+?)"'},
				'date': {'default': datetime.now()},
			})

	def info_rss(self, i):
		"""Recover the informations of a rss page"""
		self.content = self.info(i, {
			'url':         {'re': r'<yt:videoId>(.{11})</yt:videoId>'},
			'title':       {'re': r'<media:title>(.*)</media:title>'},
			'uploader':    {'re': r'<name>(.*)</name>'},
			'date':        {'re': r'<published>(.*)\+', 'date': '%Y-%m-%dT%H:%M:%S'},
			'view':        {'re': r'views="(.+?)"'},
		})
		if self.content is not None:
			self.content['view'] = self.content['view'].replace(',', '')

	def write(self):
		"""Write the information in a file"""
		self.content['image'] = 'https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.content['url'])
		self.content['url'] = 'https://www.youtube.com/watch?v=' + self.content['url']
		self.content['url_uploader'] = self._full_url()
		self.file.add(**self.content)

	def _type_id(self, id):
		"""True = Channel; False = Playlist"""
		if re.match(self.RE_CHANNEL, id):
			return True
		elif re.match(self.RE_PLAYLIST, id):
			return False
		else:
			return True

	def date_convert(self, date):
		"""
		Convert "2 day ago" -> datetime format
		"""
		value, unit, _ = date.split()
		if unit in ['month', 'months']:
			unit = 'days'
			value = int(value) * 31
		elif unit in ['year', 'years']:
			unit = 'days'
			value = int(value) * 365
		elif unit in ['minute', 'hour', 'day', 'week']:
			unit += 's'
		delta = timedelta(**{unit: int(value)})
		date = datetime.now() - delta
		return date

	def old(self, sub, since):
		sub = self.extract_id(sub)
		data = download_xml(sub, self._type_id(sub))
		if data is None:
			self.subis(sub, self.ISDEAD)
		elif data == []:
			self.subis(sub, self.ISEMPTY)
		else:
			content = self.info(data[0], {
				'date': {'re': '<published>(.*)\+', 'date':'%Y-%m-%dT%H:%M:%S'},
				'name': {'re': '<name>(.+?)</name>'},
			})
			if content is None:
				log.Error('Fail to parse the rss feed')
			else:
				if since > content['date']:
					self.subis(content['name'], content['date'])
				else:
					self.subis(content['name'], self.ISOK)

	def dead(self, sub):
		""" Print the dead channel """
		sub = self.extract_id(sub)
		linfo = download_xml(sub, self._type_id(sub))
		if linfo is None:
			self.subis(sub, self.ISDEAD)
		elif linfo is []:
			self.subis(sub, self.ISEMPTY)
		else:
			self.subis(sub, self.ISOK)
