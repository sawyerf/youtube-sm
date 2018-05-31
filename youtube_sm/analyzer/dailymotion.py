import re
from time import strptime
from ..src.sock import download_xml_daily

class Dailymotion_Analyzer(Thread)
	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
		self.id = url_id
		self.mode = mode # html / raw / list / view
		self.method = method # 0 --> RSS / 1 --> html / 2 --> ultra-html
		self.min_date = min_date
		# Init info videos
		self.url = "" # id of a video
		self.url_channel = "" 
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
			
	def write(self):
		"""Write the information in a file"""
		if self.mode == 'html':
			return self.file.write(
				url=self.url,
				title=self.title,
				url_channel=self.url_channel,
				url_img=self.url,
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
			return download_xml_daily()
		else:
			return False

	def analyzer_sub(self):
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

	def info_recup_rss(self, i):
		self.url = re.findall(r'<link>(.+?)</link>', i)[0]
		self.url_channel = 'https://www.dailymotion.com/' + self.id
		self.title = re.findall(r'<media:title>(.+?)</media:title>', i)[0]
		self.channel = self.id
		x = strptime(re.findall(r'<pubDate>.{5}(.*)\ \+', i)[0], '%d %b %Y %H:%M:%S')
		self.date = str(x.tm_year) + '-' + str(x.tm_mon) + '-' + str(x.tm_mday)
		self.data_file = [self.date.replace('-', ''), str(x.tm_hour) + str(x.tm_min) + str(x.tm_sec)]
		self.view = re.findall(r'<dm:views>(.+?)</dm:views>', i)[0].replace(',', '')


