import os
import re

from threading import Thread
from ..downloader.youtube import (
	download_xml,
	download_html,
	download_show_more,
	download_html_playlist)
from ..src.tools import (
	Progress,
	Progress_loop,
	type_id,
	check_id,
	print_debug)
from ..src.time import since

class Youtube_Analyzer(Thread):
	"""It's a group of fonctions to recover the videos informations"""
	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
		self.id = url_id
		self.mode = mode # html / raw / list / view
		self.method = method # 0 --> RSS / 1 --> html / 2 --> ultra-html
		self.min_date = min_date
		self.type = self._type_id() # True --> chanel False -- > Playlist
		# Init info videos
		self.url = "" # id of a video
		self.url_channel = ""
		self.title = ""
		self.channel = ""
		self.date = ""
		self.data_file = [] #The name of the file where stock the informations in data
		# Function
		self.prog = prog # True --> loading / False --> no loading
		self.file = file

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()
		if self.prog != None:
			self.prog.add()

	def add_sub(self, sub):
		tid = type_id(sub)
		data = download_xml(sub, type_id=tid, split=False)
		if data == None:
			print("[!] The channel/playlist can't be add. It could be delete.")
			return None
		try:
			if tid:
				data = re.findall(r'<name>(.+?)</name>', data)[0]
			else:
				data = re.findall(r'<title>(.+?)</title>', data)[0]
		except:
			print("[!] The channel/playlist can't be add. It could be delete.")
			return None
		else:
			return sub + '\t' + data

	def analyzer_sub(self):
		"""Recover all the videos of a channel or a playlist
		and add the informations in $HOME/.cache/youtube_sm/data/."""
		linfo = self._download_page()
		if linfo == False or linfo == None:
			return
		if self.method == '0':
			for i in linfo:
				date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
				if self.min_date <= date:
					self.info_rss(i)
					self.write()
		elif self.method == '1':
			if self.type: #Channel
				try:
					self.channel = linfo[0].split('<title>')[1].split('\n')[0]
				except IndexError:
					print_debug('[!] Not found the title ({})'.format(self.id))
				except:
					print_debug('[!] Not found the title ({})'.format(self.id))
				del linfo[0]
			for i in linfo:
				try:
					self.info_html(i)
				except:
					print_debug('[!] Error during the retrieve of the info ({})'.format(self.id))
				else:
					self.write()
		elif self.method == '2':
			if self.type:
				try:
					self.channel = linfo[0].split('<title>')[1].split('\n')[0]
				except IndexError:
					print_debug('[!] Not found the title ({})'.format(self.id))
				except:
					print_debug('[!] Not found the title ({})'.format(self.id))
				del linfo[0]
				for i in linfo:
					try:
						self.info_html(i)
					except:
						print_debug('[!] Error during the retrieve of the info ({})'.format(self.id))
					else:
						self.write()
				try:
					self.next = re.findall(r'data-uix-load-more-href="([^"]*)"', linfo[-1])[0]
				except:
					return
				self.show_more()
			else:
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
		if self.mode == 'html':
			return self.file.write(
				url='https://www.youtube.com/watch?v='+self.url,
				title=self.title,
				url_channel=self._complet_url_channel(self.url_channel),
				url_img='https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url),
				channel=self.channel,
				date=self.date,
				data_file=self.data_file)
		elif self.mode == 'json':
			return self.file.write(
				title=self.title,
				url=self.url,
				url_channel=self.url_channel,
				channel=self.channel,
				date=self.date,
				url_img='https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url),
				view=self.view,
				data_file=self.data_file)
		elif self.mode == 'raw':
			return self.file.write(
				url=self.url,
				title=self.title,
				url_channel=self.url_channel,
				channel=self.channel,
				date=self.date,
				data_file=self.data_file)
		elif self.mode == 'list':
			return self.file.write(
				url='https://www.youtube.com/watch?v='+self.url,
				data_file=self.data_file)
		elif self.mode == 'view':
			return self.file.write(view=self.view)

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
						print_debug('[!] Error during the retrieve of the info ({})'.format(self.id))
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
		self.date = re.findall(r'/li\\u003e\\u003cli\\u003e(.*)\\u003c\\/li', i)[0]
		self.view = re.findall(r'class="yt-lockup-meta-info"\\u003e\\u003cli\\u003e(.+?) views', i)[0].replace(',', '')
		self.data_file = [self.date_convert(), '000000']

	def info_html(self, i):
		"""Recover the informations of the html page"""
		if self.type: #Channel
			self.url = re.findall(r'href="/watch\?v=(.{11})"', i)[0]
			self.url_channel = self.id
			self.title = re.findall(r'dir="ltr" title="(.+?)"', i)[0]
			self.date = re.findall(r'</li><li>(.+?)</li>', i)[0]
			self.view = re.findall(r'class="yt-lockup-meta-info"><li>(.+?)\ views', i)[0].replace(',', '')
			self.data_file = [self.date_convert(), '000000']
		else: #Playlist
			self.url = re.findall(r'data-video-id="(.{11})"', i)[0]
			self.title = re.findall(r'data-video-title="(.+?)"', i)[0]
			self.channel = re.findall(r'data-video-username="(.+?)"', i)[0]
			self.url_channel = 'results?sp=EgIQAkIECAESAA%253D%253D&search_query=' + self.channel.replace(' ', '+')
			self.data_file = ['0000000000', '000000']

	def info_rss(self, i):
		"""Recover the informations of a rss page"""
		self.url = re.findall(r'<yt:videoId>(.{11})</yt:videoId>', i)[0]
		self.url_channel = re.findall(r'<yt:channelId>(.*)</yt:channelId>', i)[0]
		self.title = re.findall(r'<media:title>(.*)</media:title>', i)[0]
		self.channel = re.findall(r'<name>(.*)</name>', i)[0]
		self.data_file = re.findall(r'<published>(.*)\+', i)[0].replace(':', '').split('T')
		self.date = self.data_file[0]
		self.view = re.findall(r'views="(.+?)"', i)[0].replace(',', '')
		self.data_file[0] = self.data_file[0].replace('-', '')

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
				raise Exception('[*] The mode view don\' work with playlist')
			else:
				raise Exception('[*] You don\'t specify the mode')

	def _type_id(self):
		return type_id(self.id)

	def _complet_url_channel(self, url_channel):
		if url_channel[:2] == 'UC':
			url_channel = 'https://youtube.com/channel/' + url_channel
		elif url_channel[:8] == 'results?':
			url_channel = 'https://youtube.com/' + url_channel
		else:
			url_channel = 'https://youtube.com/user/' + url_channel
		return url_channel

	def date_convert(self):
		""" Convert the date which are recover in the html page
		in a date we can easily sort.
		like this: '2 day' --> '20180525'
		           '2 months' --> '20180300' 
		           '2 years' --> '20160000' """
		sdate = self.date.split(' ')
		if 'year' in sdate[1]:
			day = 365*int(sdate[0])
			return since(day)[:4] + '0000'
		elif 'month' in sdate[1]:
			day = 31*int(sdate[0])
			return since(day)[:6] + '00'
		elif 'week' in sdate[1]:
			day = 7*int(sdate[0])
		elif 'day' in sdate[1]:
			day = int(sdate[0])
		elif 'hour' in sdate[1]:
			day = 0
		elif 'minute' in sdate[1]:
			day = 0
		else:
			return '0'
		return since(day)[:8]

	def old(self, url, lcl):
		linfo = download_xml(url)
		if linfo == False:
			print('[channel dead]', url)
		elif linfo == None:
			print('[  no video  ]', url)
		else:
			tps_vd = linfo[0].split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', '')
			if lcl > int(tps_vd):
				try:
					print('[ ' + tps_vd[:4] + '/' + tps_vd[4:6] + '/' + tps_vd[6:8] + ' ] ' + linfo[0].split('<name>')[1].split('</name>')[0])
				except UnicodeEncodeError:
					print('[ ' + tps_vd[:4] + '/' + tps_vd[4:6] + '/' + tps_vd[6:8] + ' ]', linfo[0].split('<name>')[1].split('</name>')[0].encode())
				except:
					print("[   erreur   ]", url)

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
		raw = data.split("<media:community>")[1].split("</media:community>")[0]
		try:
			mark = float(data.split("average=\"")[1].split("\"")[0])
		except:
			mark = None
		try:
			view = int(data.split("views=\"")[1].split("\"")[0])
		except:
			view = 0
		return mark, view
