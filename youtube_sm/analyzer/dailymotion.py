import re

from time			import strptime
from threading			import Thread
from .analyzer			import Analyzer
from ..core.tools		import log
from ..downloader.dailymotion	import download_xml_daily

class Dailymotion_Analyzer(Thread, Analyzer):
	SITE='[dailymotion]'
	URL_MATCH=r'(https://|)(www\.|)dailymotion\.com/'

	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
		self.id		 = url_id
		self.mode	 = mode # html / raw / list / view
		self.method	 = method # 0 --> RSS / 1 --> html / 2 --> ultra-html
		self.min_date	 = min_date
		# Init info videos
		self.url	 = "" # id of a video
		self.url_channel = ""
		self.url_img	 = ""
		self.title	 = ""
		self.channel	 = ""
		self.date	 = ""
		self.data_file	 = "" #The name of the file where stock the informations in data
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
		log.Warning("Dailymotion has delete the rss so this functionnality is suspende. Sorry")
		return None
		data = download_xml_daily(sub, split=False)
		if data == None:
			return None
		return sub + '\t' + sub

	def analyzer_sub(self):
		log.Warning("Dailymotion has delete the rss so this functionnality is suspende. Sorry")
		return
		if self.method == '0':
			linfo = self._download_page()
			print(linfo)
			if linfo == False or linfo == None:
				return
			for i in linfo:
				try:
					self.info_recup_rss(i)
				except:
					lor.warning('Error during the retrieve of the info ({})'.format(self.id))
				else:
					self.write()

	def _download_page(self):
		if self.method == '0':
			return download_xml_daily(self.id)
		else:
			return False

	def write(self):
		"""Write the information in a file"""
		return self.file.write(
			channel=self.channel,
			data_file=self.data_file,
			date=self.date,
			title=self.title,
			url=self.url,
			url_channel=self.url_channel,
			url_img=self.url_img,
			view=self.view,
		)

	def info_recup_rss(self, i):
		self.url = re.findall(r'<link>(.+?)</link>', i)[0]
		self.url_channel = 'https://www.dailymotion.com/' + self.id
		self.title = re.findall(r'<media:title>(.+?)</media:title>', i)[0]
		self.url_img = re.findall(r'<media:thumbnail\ url="(.+?)"', i)[0]
		self.channel = self.id
		self.date, x = self.convert_date(re.findall(r'<pubDate>.{5}(.*)\ \+', i)[0], True)
		self.data_file = [self.date.replace('-', ''), str(x.tm_hour) + str(x.tm_min) + str(x.tm_sec)]
		self.view = re.findall(r'<dm:views>(.+?)</dm:views>', i)[0].replace(',', '')

	def convert_date(self, date, y=False):
		x = strptime(date, '%d %b %Y %H:%M:%S')
		month, day = str(x.tm_mon), str(x.tm_mday)
		if len(month) == 1:
			month = '0' + month
		if len(day) == 1:
			day = '0' + day
		if y:
			return str(x.tm_year) + '-' + month + '-' + day, x
		else:
			return str(x.tm_year) + '-' + month + '-' + day

	def old(self, url, lcl):
		data = download_xml_daily(url)
		if data == None:
			print('[ channel dead ]', url)
		else:
			try:
				last = int(self.convert_date(re.findall(r'<pubDate>.{5}(.*)\ \+', data[0])[0]).replace('-', ''))
			except:
				return
			if last <= lcl:
				last = str(last)
				print('[ ' + last[:4] + '/' + last[4:6] + '/' + last[6:8] + ' ] ' + url)
		return

	def dead(self, url):
		data = download_xml_daily(url)
		if data == None or data == False:
			print('[ channel dead ]', url)

	def stat(self, sub, name=''):
		view, like = 0, 0
		data = download_xml_daily(sub, False)
		views = re.findall(r'views>(.+?)</dm', data)
		likes = re.findall(r'dm:favorites>(.+?)</', data)
		for i in views:
			try:
				view += int(i)
			except:
				pass
		for i in likes:
			try:
				like += int(i)
			except:
				pass
		print(like, 'likes for', sub, '(' + str(view) + ' views)')
