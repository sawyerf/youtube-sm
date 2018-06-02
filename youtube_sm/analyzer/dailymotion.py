import re
from time import strptime
from threading import Thread

from ..src.sock import download_xml_daily

class Dailymotion_Analyzer(Thread):
	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
		self.id = url_id
		self.mode = mode # html / raw / list / view
		self.method = method # 0 --> RSS / 1 --> html / 2 --> ultra-html
		self.min_date = min_date
		# Init info videos
		self.url = "" # id of a video
		self.url_channel = "" 
		self.url_img = ""
		self.title = ""
		self.channel = ""
		self.date = ""
		self.data_file = "" #The name of the file where stock the informations in data
		# Function
		self.prog = prog # True --> loading / False --> no loading
		self.file = file

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()
		if self.prog != None:
			self.prog.add()
			
	def analyzer_sub(self):
		if self.method == '0':
			linfo = self._download_page()
			if linfo == False or linfo == None:
				return
			for i in linfo:
				try:
					self.info_recup_rss(i)
				except:
					continue
				else:
					self.write()

	def write(self):
		"""Write the information in a file"""
		if self.mode == 'html':
			return self.file.write(
				url=self.url,
				title=self.title,
				url_channel=self.url_channel,
				url_img=self.url_img,
				channel=self.channel,
				date=self.date,
				data_file=self.data_file)
		elif self.mode == 'raw':
			return self.file.write(
				url=self.url,
				title=self.title,
				url_channel=self.url_channel,
				channel=self.channel,
				date=self.date,
				data_file=self.data_file,
				type_id=self.type)
		elif self.mode == 'list':
			return self.file.write(
				url=self.url,
				data_file=self.data_file,
				type_id=self.type)
		elif self.mode == 'view':
			return self.file.write(view=self.view)

	def _download_page(self):
		if self.method == '0':
			return download_xml_daily(self.id)
		else:
			return False

	def info_recup_rss(self, i):
		self.url = re.findall(r'<link>(.+?)</link>', i)[0]
		self.url_channel = 'https://www.dailymotion.com/' + self.id
		self.title = re.findall(r'<media:title>(.+?)</media:title>', i)[0]
		self.url_img = re.findall(r'<media:thumbnail\ url="(.+?)"', i)[0]
		self.channel = self.id
		x = strptime(re.findall(r'<pubDate>.{5}(.*)\ \+', i)[0], '%d %b %Y %H:%M:%S')
		self.date = self.convert_date(x)
		self.data_file = [self.date.replace('-', ''), str(x.tm_hour) + str(x.tm_min) + str(x.tm_sec)]
		self.view = re.findall(r'<dm:views>(.+?)</dm:views>', i)[0].replace(',', '')

	def convert_date(self, x):
		month, day = str(x.tm_mon), str(x.tm_mday)
		if len(month) == 1:
			month = '0' + month
		if len(day) == 1:
			day = '0' + day
		return str(x.tm_year) + '-' + month + '-' + day
