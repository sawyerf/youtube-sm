import os
import time
import re

from threading import Thread
from .sock import (
	download_xml,
	download_html,
	download_show_more,
	download_html_playlist)
from .tools import (
	Progress,
	Progress_loop,
	type_id)
from .time import since


def html_init(path, output='sub.html'):
	"""To init the html file"""
	open(output, 'w').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="css/sub.css" />
		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>
		<title>Abonnements</title>
	</head>
	<body>
<!-- {} -->
""".format(time.ctime()))

def init(urls, output, min_date, path='', mode='html', loading=False, method='0'):
	"""Run all the analyze in a thread"""
	threads = []
	ending = 0
	nb = len(urls)
	if loading and nb == 1:
		prog = Progress_loop()
		prog.progress_bar()
	elif loading and nb > 1:
		prog = Progress(nb)
		prog.progress_bar()
	if method == '0':
		max_thr = 200
	elif method == '1':
		max_thr = 50
	elif method == '2':
		max_thr = 5
	for i in range(nb):
		if loading:
			thr = Analyzer(mode, urls[i], output, min_date, method, path, prog)
		else:
			thr = Analyzer(mode, urls[i], output, min_date, method, path)
		thr.Thread()
		threads.append(thr)
		thr.start()
		if i%max_thr == 0 or nb == i+1:
			for y in threads:
				y.join()
			threads = []
	if loading and prog.xmin != prog.xmax:
		prog.xmin = prog.xmax
		prog.progress_bar()


class Analyzer(Thread):
	"""It's a group of fonctions to recover the videos informations"""
	def __init__(self, mode='', url_id='', output='', min_date=0, method='0', path='', prog=None):
		self.mode = mode # html / raw / list / view
		self.method = method # 0 --> RSS / 1 --> html / 2 --> ultra-html
		self.id = url_id
		if output != '':
			self.output = output
		else:
			if mode == 'html':
				self.output = 'sub.html'
			elif mode == 'list':
				self.output = 'sub_list'
			elif mode == 'raw':
				self.output = 'sub_raw'
			elif mode == 'view':
				self.output = 'sub_view'
			else:
				self.output = 'sub'
		self.path_cache = path # The path where the data and the sub are stock
		self.min_date = min_date 
		self.type = self._type_id() # True --> chanel False -- > Playlist
		#all the var user in class
		self.url = "" # id of a video
		self.url_channel = "" 
		self.title = ""
		self.channel = ""
		self.date = ""
		self.data_file = "" #The name of the file where stock the informations in data
		#Progress
		self.prog = prog # True --> loading / False --> no loading

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()
		if self.prog != None:
			self.prog.add()

	def _type_id(self):
		return type_id(self.id)

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

	def analyzer_sub(self):
		"""Recover all the videos of a channel or a playlist
		and add the informations in $HOME/.cache/youtube_sm/data/."""
		linfo = self._download_page()
		if linfo == False or linfo == None:
			return
		try:
			os.mkdir(self.path_cache + 'data/' + self.method)
		except:
			pass
		if self.method == '0':
			for i in linfo:
				date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
				if self.min_date <= date:
					self.info_recup_rss(i)
					if self.mode == 'view':
						self.write(i)
					else:
						self.write()
		elif self.method == '1':
			if self.type: #Channel
				try:
					self.channel = linfo[0].split('<title>')[1].split('\n')[0]
				except IndexError:
					pass
				except:
					pass
				del linfo[0]
			for i in linfo:
				try:
					self.info_recup_html(i)
				except:
					pass
				else:
					if self.mode == 'view':
						self.write(i)
					else:
						self.write()
		elif self.method == '2':
			if self.type:
				try:
					self.channel = linfo[0].split('<title>')[1].split('\n')[0]
				except IndexError:
					pass
				except:
					pass
				del linfo[0]
				for i in linfo:
					try:
						self.info_recup_html(i)
					except:
						pass
					else:
						if self.mode == 'view':
							self.write(i)
						else:
							self.write()
				self.next = re.findall(r'data-uix-load-more-href="(.{176})"', linfo[-1])[0]
				self.show_more()
			else:
				self.show_more()

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
						self.info_recup_show_more(i)
					except:
						pass
					else:
						if self.mode == 'view':
							self.write(i)
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
							self.info_recup_html(i)
						else:
							continue
					except:
						pass
					else:
						if self.mode == 'view':
							self.write(i)
						else:
							self.write()
				if self.prog != None:
					self.prog.add()

	def info_recup_show_more(self, i):
		"""Recover the informations for the mode 'ultra-html'"""
		self.url = re.findall(r'href="\\/watch\?v=(.{11})"', i)[0]
		self.url_channel = self.id
		self.title = re.findall(r'ltr"\ title="(.+?)"', i)[0]
		self.date = re.findall(r'/li\\u003e\\u003cli\\u003e(.*)\\u003c\\/li', i)[0]
		self.data_file = [self.date_convert(), 'no_hour']

	def info_recup_html(self, i):
		"""Recover the informations of the html page"""
		if self.type: #Channel
			self.url = re.findall(r'href="/watch\?v=(.{11})"', i)[0]
			self.url_channel = self.id
			self.title = re.findall(r'dir="ltr" title="(.+?)"', i)[0]
			self.date = re.findall(r'</li><li>(.+?)</li>', i)[0]
			self.data_file = [self.date_convert(), 'no_hour']
		else: #Playlist
			self.url = re.findall(r'data-video-id="(.{11})"', i)[0]
			self.title = re.findall(r'data-video-title="(.+?)"', i)[0]
			self.channel = re.findall(r'data-video-username="(.+?)"', i)[0]
			self.url_channel = 'results?sp=EgIQAkIECAESAA%253D%253D&search_query=' + self.channel.replace(' ', '+')
			self.data_file = ['Playlist', self.id]

	def info_recup_rss(self, i):
		"""Recover the informations of a rss page"""
		self.url = re.findall(r'<yt:videoId>(.{11})</yt:videoId>', i)[0]
		self.url_channel = re.findall(r'<yt:channelId>(.*)</yt:channelId>', i)[0]
		self.title = re.findall(r'<media:title>(.*)</media:title>', i)[0]
		self.channel = re.findall(r'<name>(.*)</name>', i)[0]
		self.data_file = re.findall(r'<published>(.*)\+', i)[0].split('T')
		self.date = self.data_file[0]
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

	def write(self, i=None):
		"""Write the information in a file"""
		if self.mode == 'html':
			return self.generate_data_html()
		elif self.mode == 'raw':
			return self.append_raw()
		elif self.mode == 'list':
			return self.append_list()
		elif self.mode == 'view':
			return self.append_view(i)

	def append_raw(self):
		"""Append the informations wich are been recover 
		in the file 'sub_raw'."""
		if self.method == '0':
			var = self.data_file[0] + self.data_file[1].replace(':', '') + '\t' + self.date + '\t' + self.url + '\t' + self.url_channel + '\t' + self.title + '\t' + self.channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url) + '\n'
			if len(var) > 350:
				return False
			open(self.output, 'a', encoding='utf8').write(var)
		elif self.method == '1' or self.method == '2':
			if self._type_id == True:
				var = self.data_file[0] + '000000' + '\t' + self.url + '\t' + self.url_channel + '\t' + self.title + '\t' + self.channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url) + '\n'
			else:
				var = '00000000000000' + '\t' + self.url + '\t' + self.url_channel + '\t' + self.title + '\t' + self.channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url) + '\n'
			if len(var) > 350:
				return False
			open(self.output, 'a', encoding='utf8').write(var)
		var = ""
		return True

	def append_list(self):
		""""Append the informations wich are been recover
		in the file 'sub_raw'. The date is add to sort the
		videos, but it's deleted"""
		if len(self.url) != 11:
			return False
		if self.method == '0':
			open(self.output, 'a', encoding='utf8').write(self.data_file[0] + self.data_file[1].replace(':', '') + ' https://www.youtube.com/watch?v=' + self.url + '\n')
		elif self.method == '1' or self.method == '2':
			if self.type:
				open(self.output, 'a', encoding='utf8').write(self.data_file[0] + '000000' + ' https://www.youtube.com/watch?v=' + self.url + '\n')
			else:
				open(self.output, 'a', encoding='utf8').write('00000000000000' + ' https://www.youtube.com/watch?v=' + self.url + '\n')
		return True

	def append_view(self, i):
		""" Write the views in a file"""
		try:
			view = self._view(i)
		except:
			print(i)
			return
		if view != None:
			open(self.output, 'a', encoding='utf8').write(view + '\n')

	def generate_data_html(self):
		"""Append the informations wich are been recover
		in a file in '.../data/[date]/.' """
		try:
			data = open('{}data/{}/{}/{}'.format(self.path_cache, self.method, self.data_file[0], self.data_file[1].replace(':', '')), 'rb+').read().decode("utf8")
			if self.url in data:
				return False
		except:
			try:
				os.mkdir(self.path_cache + 'data/' + self.method + '/' + self.data_file[0])
			except:
				pass
		if self.url_channel[:2] == 'UC':
			self.url_channel = 'channel/' + self.url_channel
		elif self.url_channel[:8] == 'results?':
			pass
		else:
			self.url_channel = 'user/' + self.url_channel
		open('{}data/{}/{}/{}'.format(self.path_cache, self.method, self.data_file[0], self.data_file[1].replace(':', '')), 'a', encoding='utf-8').write("""<!--NEXT -->
<div class="video">
	<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="https://i.ytimg.com/vi/{}/mqdefault.jpg" ></a>
	<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
	<a href="https://www.youtube.com/{}"> <p>{}</p> </a>
	<p>{}</p>
	<p class="clear"></p>
</div>
""".format(self.url, self.url, self.url, self.title, self.url_channel, self.channel, self.date))
		return True

def sort_file(count=7, output='sub.html', mode='html', path='', method='0'):
	""" To sort the videos by date or add the videos in the file"""
	if mode == 'html':
		html_end(count, path, output, method)
	elif mode == 'list' or mode == 'raw':
		raw_list_end(count, output)

def html_end(count=7, path='', output='sub.html', method='0', play=True):
	"""Recover the file in '.../data/.' with all the
	informations, sort by date and add the informations
	in './sub.html'. """
	fch = sorted(os.listdir(path + 'data/' + method + '/'))
	if len(fch) < count:
		date = 0
	elif count == -1:
		date = -1
	else:
		date = int(since(count)[:8])
	sub_file = open(output, 'a', encoding='utf-8')
	i = -1
	while True:
		i += 1
		try:
			folder_date = int(fch[-1-i])
		except IndexError:
			break
		except:
			if play:
				folder_date = 0
			else:
				continue
		if folder_date > date:
			fch_in = sorted(os.listdir(path + 'data/' + method + '/' + fch[-1-i]))
			for a in range(len(fch_in)):
				data = open(path + 'data/' + method + '/' + fch[-1-i] + '/' + fch_in[-1-a], 'r', encoding='utf-8').read()
				sub_file.write(data)
	sub_file.close()
	open(output, 'a').write('</body></html>')

def raw_list_end(count=7, output='sub'):
	"""Sorted the videos by date"""
	linfo = sorted(open(output, 'rb').read().decode('utf8').replace('\r', '').split('\n'))
	fichier = open(output, 'w', encoding='utf8')
	if count == -1:
		date = -1
	else:
		date = int(since(count)[:8])
	i = -1
	while True:
		i += 1
		try:
			folder_date = int(linfo[-1-i][:8])
		except IndexError:
			break
		except:
			continue
		if folder_date > date:
			fichier.write(linfo[-1-i][15:] + '\n')
		else:
			break
