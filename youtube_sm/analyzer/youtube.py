import os
import re

from datetime			import datetime, timedelta
from threading			import Thread
from .analyzer			import Analyzer
from ..downloader.youtube	import (
	download_xml,
	download_html,
	download_show_more,
	download_html_playlist
)
from ..core.tools		import (
	Progress,
	Progress_loop,
	log
)

class Youtube_Analyzer(Thread, Analyzer):
	SITE='[youtube]'
	URL_MATCH=r'(?:https://|)(?:www\.|)youtube\.com/(?P<type>channel/|user/|playlist\?list=)(?P<ID>[a-zA-Z0-9_-]*)'
	RE_CHANNEL=r'UC[A-Za-z0-9_-]{22}'
	RE_PLAYLIST=r'PL[A-Za-z0-9_-]{32}'

	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
		self.id = self.extract_sub(url_id)
		self.mode = mode # html / raw / list / view
		self.method = method # 0 --> RSS / 1 --> html / 2 --> ultra-html
		self.min_date = min_date
		self.type = self._type_id(url_id) # True --> chanel False -- > Playlist
		# Init info videos
		self.channel = ''
		self.date = ''
		self.title = ''
		self.url = ''
		self.url_channel = ''
		self.url_img = ''
		self.view = ''
		# Function
		self.prog = prog # True --> loading / False --> no loading
		self.file = file

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()
		if self.prog != None:
			self.prog.add()

	def extract_sub(self, url):
		match = self.match(url)
		if match:
			return match.group('ID')
		return url

	def add_sub(self, url):
		sub = self.extract_sub(url)
		tid = self._type_id(sub)
		data = download_xml(sub, type_id=tid, split=False)
		if data == None:
			log.Error("The channel/playlist can't be add. It could be delete.")
			return None
		match = re.findall(r'<(?:title|name)>(.+?)</(?:title|name)>', data)
		if match != []:
			return sub + '\t' + match[0]
		log.Warning("The channel/playlist can't be add. It could be delete.")
		return None

	def analyzer_sub(self):
		"""Recover all the videos of a channel or a playlist
		and add the informations in $HOME/.cache/youtube_sm/data/."""
		linfo = self._download_page()
		if linfo == False or linfo == None:
			return
		if self.method == '0':
			for i in linfo:
				date = int(re.findall('<published>(.+?)</published>', i)[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
				if self.min_date <= date:
					self.info_rss(i)
					self.write()
		elif self.method == '1':
			if self.type: #Channel
				try:
					self.channel = re.findall('<title>(.*)', linfo[0])[0]
				except:
					log.Error('Not found the title ({})'.format(self.id))
				del linfo[0]
			for i in linfo:
				try:
					self.info_html(i)
					self.write()
				except:
					log.Error('Error during the retrieve of the info ({})'.format(self.id))
		elif self.method == '2':
			if self.type:
				try:
					self.channel = re.findall('<title>(.*)', linfo[0])[0]
				except:
					log.Error('Not found the title ({})'.format(self.id))
				del linfo[0]
				for i in linfo:
					try:
						self.info_html(i)
						self.write()
					except:
						log.Error('Error during the retrieve of the info ({})'.format(self.id))
				try:
					self.next = re.findall(r'data-uix-load-more-href="([^"]*)"', linfo[-1])[0]
				except:
					return
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
		""" The continuation of analyzer_sub for the mode 'ultra-html'
		This function recover and write the information recover in
		in the link in the button 'load more'"""
		data = ''
		if self.type:
			while self.next != None:
				data, self.next = download_show_more(self.next, True)
				if data == None:
					return
				for i in data:
					try:
						self.info_show_more(i)
					except:
						log.Error('Error during the retrieve of the info ({})'.format(self.id))
					else:
						self.write()
				if self.prog != None:
					self.prog.add()
		else:
			nb = 0
			while nb < self.len_play:
				data, self.next = download_show_more(self.next, False)
				if data == None:
					return
				for i in data:
					try:
						if nb < int(re.findall(r'tch\?v=.*;index=([0-9]+)', i)[0]):
							nb += 1
							self.info_html(i)
						else:
							continue
					except:
						pass
					else:
						self.write()
				if self.prog != None:
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
		if self.type: #Channel
			self.url			= re.findall(r'href="/watch\?v=(.{11})"', i)[0]
			self.url_channel	= self.id
			self.title			= re.findall(r'dir="ltr" title="(.+?)"', i)[0]
			date				= re.findall(r'</li><li>(.+?)</li>', i)[0]
			self.date			= self.date_convert(date)
			self.view			= re.findall(r'class="yt-lockup-meta-info"><li>(.+?)\ views', i)[0].replace(',', '')
		else: #Playlist
			self.url			= re.findall(r'data-video-id="(.{11})"', i)[0]
			self.title			= re.findall(r'data-video-title="(.+?)"', i)[0]
			self.channel		= re.findall(r'data-video-username="(.+?)"', i)[0]
			self.url_channel	= self.id
			self.date			= datetime.now()

	def info_rss(self, i):
		"""Recover the informations of a rss page"""
		self.url			= re.findall(r'<yt:videoId>(.{11})</yt:videoId>', i)[0]
		self.url_channel	= re.findall(r'<yt:channelId>(.*)</yt:channelId>', i)[0]
		self.title			= re.findall(r'<media:title>(.*)</media:title>', i)[0]
		self.channel		= re.findall(r'<name>(.*)</name>', i)[0]
		date				= re.findall(r'<published>(.*)\+', i)[0]
		self.date			= datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
		self.view			= re.findall(r'views="(.+?)"', i)[0].replace(',', '')

	def _view(self, i):
		""" Return the views of a videos"""
		if self.method == '0':
			return re.findall(r'views="(.+?)"', i)[0].replace(',', '')
		elif self.method == '1' and self.type:
			return re.findall(r'class="yt-lockup-meta-info"><li>(.+?)\ views', i)[0].replace(',', '')
		elif self.method == '2' and self.type:
			if '<ul class="yt-lockup-meta-info"><li>' in i:
				return re.findall(r'class="yt-lockup-meta-info"><li>(.+?) views', i)[0].replace(',', '')
			elif 'class="yt-lockup-meta-info"\\u003e\\u003cli\\u003e' in i:
				return re.findall(r'class="yt-lockup-meta-info"\\u003e\\u003cli\\u003e(.+?) views', i)[0].replace(',', '')
		else:
			if not self.type:
				raise Exception('[!] The mode view don\' work with playlist')
			else:
				raise Exception('[!] You don\'t specify the mode')

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
		if linfo == False:
			print('[channel dead]', url)
		elif linfo == None:
			print('[  no video  ]', url)
		else:
			tps_vd = re.findall(r'<published>([0-9-]{10})T.+?</published>', linfo[0])[0]
			if lcl > int(tps_vd.replace('-', '')):
				print('[ {} ] {}'.format(tps_vd.replace('-', '/'), re.findall('<name>(.+?)</name>', linfo[0])[0]))

	def dead(self, url):
		""" Print the dead channel """
		linfo = download_xml(url)
		if linfo == False:
			print('[channel dead]\t', url)
		elif linfo == None:
			print('[  no video  ]\t', url)


	def stat(self, sub, name=''):
		"""Print the mark and the views of a channel"""
		data = download_xml(sub)
		if data == None or data == False:
			return
		marks = 0
		views = 0
		count_marks = 0
		for i in data:
			mark, view = self.info_stats(i)
			if mark != None:
				marks += mark
				count_marks += 1
			views += view
		marks = marks / (count_marks / 2)
		prin = str(marks)[:4] + " for " + name + ' (' + str(views) + ' views)'
		try:
			print(prin)
		except:
			print(prin.encode())


	def info_stats(self, data):
		try:
			mark = float(re.findall('average="(.+?)"', data)[0])
			view = int(re.findall('views="(.+?)"', data)[0])
		except:
			return None, None
		return mark, view
