import	re

from	threading	import	Thread
from	datetime	import	datetime
from	..src.sock	import	(
			download_https)
from ..src.tools import print_debug

def ptube_crtlink(info, type_file):
	if len(info) == 2 and info[1] != '':
		return '/feeds/videos.{}?accountId={}'.format(type_file, info[1])
	return '/feeds/videos.{}'.format(type_file)

def	download_xml_peertube(url_id, split=True):
	info = url_id.split(':')
	print(ptube_crtlink(info, 'xml'))
	data = download_https(ptube_crtlink(info, 'xml').encode(), info[0])
	if data == None:
		print_debug('[!] Failed to download (url_id)')
		return None
	if split:
		linfo = data.split('<item>')
		del linfo[0]
		if linfo == []:
			return None
		return linfo
	else:
		return data

def	download_atom_peertube(url_id, split=True):
	info = sub.split(':')
	data = download_https(ptube_crtlink(info, 'atom').encode(), info[0])
	if data == None:
		return None
	if split:
		linfo = data.split('<item>')
		del linfo[0]
		if linfo == []:
			return None
		return linfo
	else:
		return data

class	Peertube_Analyzer(Thread):
	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
		###################### 
		# The basic variable #
		######################
		self.id = url_id
		self.mode = mode 
		self.method = method 
		self.min_date = min_date
		###############################
		# Init the video informations #
		###############################
		self.url = ""
		self.url_channel = "" 
		self.title = ""
		self.channel = ""
		self.date = ""
		self.data_file = "" 
		################
		# The function #
		################
		self.prog = prog
		self.file = file

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()
		if self.prog != None:
			self.prog.add()

	def add_sub(self, sub):
		""" This function return the informations wich are write in sub.swy ."""
		data = download_xml_peertube(sub, False)
		if data == None:
			print("[!] The channel/playlist can't be add. It could be delete.")
			return 'None'
		try:
			data = re.findall(r'<title>(.*)</title>', data)[0]
		except:
			print("[!] The channel/playlist can't be add. It could be delete.")
			return None
		else:
			return sub + '\t' + data

	def	_download_page(self):
		if self.method == '0':
			return download_xml_peertube(self.id)
		else:
			return False

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
		elif self.mode == 'json':
			return self.file.write(
				title=self.title,
				url=self.url,
				url_channel=self.url_channel,
				channel=self.channel,
				date=self.date,
				url_img=self.url_img,
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
				url=self.url,
				data_file=self.data_file)
		elif self.mode == 'view':
			return None

	def analyzer_sub(self):
		""" The main function  wich retrieve the informations and and write it
		in a file"""
		if self.method == '0':
			linfo = self._download_page()
			if linfo == False or linfo == None:
				return
			for i in linfo:
				try:
					self.info_rss(i)
				except:
					print_debug('[!] Error during the retrieve of the info ({})'.format(self.id))
				else:
					self.write()

	def info_rss(self, i):
		self.url =			re.findall(r'<link>(.*)</link>', i)[0]
		self.url_channel =	'https://' + self.id.split(':')[0]
		self.channel =		re.findall(r'<dc:creator>(.*)</dc:creator>', i)[0]
		self.title =		re.findall(r'<title><!\[CDATA\[(.*)\]\]></title>', i)[0]
		self.url_img =		re.findall(r'<media:thumbnail url="(.*)"', i)[0]
		self.date =			re.findall(r'<pubDate>(.*)</pubDate>', i)[0]
		date =				datetime.strptime(self.date, '%a, %d %b %Y %H:%M:%S GMT')
		self.date = 		date.strftime("%Y-%m-%d")
		self.data_file =	[date.strftime("%Y%m%d"), date.strftime("%H%M%S")]

	def old(self, url, lcl):
		""" The function wich is call with the option -o 
		This function print the old channel or the dead channel."""
		pass

	def dead(self, url):
		""" The function wich is call with the option -d 
		This function print the dead channel."""
		pass

	def stat(self, sub, name):
		""" The function wich is call with the option -s
		This function print the views and the ratio of like of a video"""
		pass
