import re

from datetime     import datetime, timedelta
from ..core.tools import log
from .analyzer    import Analyzer
from ..downloader.youtube import (
	download_xml,
	download_html,
	download_show_more,
	download_html_playlist
)


class Youtube_Analyzer(Analyzer):
	SITE='[youtube]'
	URL_MATCH=r'(?:https://|)(?:www\.|)youtube\.com/(?P<type>channel/|user/|playlist\?list=)(?P<ID>[a-zA-Z0-9_-]*)'
	RE_CHANNEL=r'UC[A-Za-z0-9_-]{22}'
	RE_PLAYLIST=r'PL[A-Za-z0-9_-]{32}'

	def __init__(self, url_id='', method='0', file=None, prog=None):
		self.id = self.extract_id(url_id)
		self.method = method
		self.type = self._type_id(url_id)  # True --> chanel False -- > Playlist
		# Init info videos
		self.channel = ''
		self.date = ''
		self.title = ''
		self.url = ''
		self.url_channel = ''
		self.url_img = ''
		self.view = ''
		# Function
		self.prog = prog
		self.file = file

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
		linfo = self._download_page()
		if linfo is False or linfo is None:
			return
		if self.method == '0':
			for i in linfo:
				self.info_rss(i)
				self.write()
		elif self.method == '1':
			if self.type:  # Channel
				channel = re.findall('<title>(.*)', linfo[0])
				if channel == []:
					log.Error('Title not found ({})'.format(self.id))
				else:
					self.channel = channel[0]
				del linfo[0]
			for i in linfo:
				try:
					self.info_html(i)
					self.write()
				except:
					log.Error('Error during the retrieve of the info ({})'.format(self.id))
		elif self.method == '2':
			if self.type:
				channel = re.findall('<title>(.*)', linfo[0])[0]
				if channel == []:
					log.Error('Title not found ({})'.format(self.id))
				else:
					self.channel = channel[0]
				del linfo[0]
				for i in linfo:
					try:
						self.info_html(i)
						self.write()
					except:
						log.Error('Error during the retrieve of the info ({})'.format(self.id))
				nexts = re.findall(r'data-uix-load-more-href="([^"]*)"', linfo[-1])
				if nexts == []:
					return
				self.next = nexts[0]
			self.show_more()

	def _download_page(self):
		""" To download a page with the id of a channel/Playlist """
		if self.method == '0':
			return download_xml(self.id, self.type)
		elif self.method == '1':
			return download_html(self.id, self.type)
		elif self.method == '2':
			if self.type:
				return download_html(self.id, self.type)
			else:
				linfo, self.next, self.len_play = download_html_playlist(self.id)
				return linfo
		else:
			return None

	def write(self):
		"""Write the information in a file"""
		return self.file.add(
			uploader=self.channel,
			date=self.date,
			title=self.title,
			url='https://www.youtube.com/watch?v='+self.url,
			url_uploader=self._complet_url_channel(self.url_channel),
			image='https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url),
			view=self.view,
		)

	def show_more(self):
		""" The continuation of real_analyzer for the mode 'ultra-html'
		This function recover and write the information recover in
		in the link in the button 'load more'"""
		data = ''
		if self.type:
			while self.next is not None:
				data, self.next = download_show_more(self.next, True)
				if data is None:
					return
				for i in data:
					try:
						self.info_show_more(i)
						self.write()
					except:
						log.Error('Error during the retrieve of the info ({})'.format(self.id))
				if self.prog is not None:
					self.prog.add()
		else:
			nb = 0
			while nb < self.len_play:
				data, self.next = download_show_more(self.next, False)
				if data is None:
					return
				for i in data:
					index = re.findall(r'tch\?v=.*;index=([0-9]+?)', i)
					if index != [] and nb < int(index[0]):
						nb += 1
						try:
							self.info_html(i)
							self.write()
						except:
							log.Error('Error during the retrieve of the info ({})'.format(self.id))
				if self.prog is not None:
					self.prog.add()
		print()

	def info_show_more(self, i):
		"""Recover the informations for the mode 'ultra-html'"""
		self.url = re.findall(r'href="\\/watch\?v=(.{11})"', i)[0]
		self.url_channel = self.id
		self.title = re.findall(r'ltr"\ title="(.+?)"', i)[0]
		date = re.findall(r'/li\\u003e\\u003cli\\u003e(.*)\\u003c\\/li', i)[0]
		self.date = self.date_convert(date)
		self.view = re.findall(r'class="yt-lockup-meta-info"\\u003e\\u003cli\\u003e(.+?) views', i)[0].replace(',', '')

	def info_html(self, i):
		"""Recover the informations of the html page"""
		if self.type:  # Channel
			self.url         = re.findall(r'href="/watch\?v=(.{11})"', i)[0]
			self.url_channel = self.id
			self.title       = re.findall(r'dir="ltr" title="(.+?)"', i)[0]
			date             = re.findall(r'</li><li>(.+?)</li>', i)[0]
			self.date        = self.date_convert(date)
			self.view        = re.findall(r'class="yt-lockup-meta-info"><li>(.+?)\ views', i)[0].replace(',', '')
		else:  # Playlist
			self.url         = re.findall(r'data-video-id="(.{11})"', i)[0]
			self.title       = re.findall(r'data-video-title="(.+?)"', i)[0]
			self.channel     = re.findall(r'data-video-username="(.+?)"', i)[0]
			self.url_channel = self.id
			self.date        = datetime.now()

	def info_rss(self, i):
		"""Recover the informations of a rss page"""
		self.url         = re.findall(r'<yt:videoId>(.{11})</yt:videoId>', i)[0]
		self.url_channel = re.findall(r'<yt:channelId>(.*)</yt:channelId>', i)[0]
		self.title       = re.findall(r'<media:title>(.*)</media:title>', i)[0]
		self.channel     = re.findall(r'<name>(.*)</name>', i)[0]
		date             = re.findall(r'<published>(.*)\+', i)[0]
		self.date        = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
		self.view        = re.findall(r'views="(.+?)"', i)[0].replace(',', '')

	def _type_id(self, id):
		"""True = Channel; False = Playlist"""
		if re.match(self.RE_CHANNEL, id):
			return True
		elif re.match(self.RE_PLAYLIST, id):
			return False
		else:
			return True

	def _complet_url_channel(self, url_channel):
		if url_channel[:2] == 'UC':
			url_channel = 'https://youtube.com/channel/' + url_channel
		elif url_channel[:8] == 'results?':
			url_channel = 'https://youtube.com/' + url_channel
		else:
			url_channel = 'https://youtube.com/user/' + url_channel
		return url_channel

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

	def old(self, url, lcl):
		linfo = download_xml(url)
		if linfo is False:
			print('[channel dead]', url)
		elif linfo is None:
			print('[  no video  ]', url)
		else:
			tps_vd = re.findall(r'<published>([0-9-]{10})T.+?</published>', linfo[0])[0]
			if lcl > int(tps_vd.replace('-', '')):
				print('[ {} ] {}'.format(tps_vd.replace('-', '/'), re.findall('<name>(.+?)</name>', linfo[0])[0]))

	def dead(self, url):
		""" Print the dead channel """
		linfo = download_xml(url)
		if linfo is False:
			print('[channel dead]\t', url)
		elif linfo is None:
			print('[  no video  ]\t', url)
