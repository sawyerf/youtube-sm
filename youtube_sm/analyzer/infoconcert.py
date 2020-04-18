import re
from threading		import Thread
from .analyzer			import Analyzer
from ..downloader.infoconcert	import (
	download_html_infoconcert
)
from ..core.tools	import (
	log
)

class InfoConcert_Analyzer(Thread, Analyzer):
	SITE='[infoconcert]'
	URL_MATCH=r'(?:https://|)(?:www\.|)infoconcert\.com/artiste/(?P<ID>[a-z-]*[0-9]*)/.*\.html'

	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
		######################
		# The basic variable #
		######################
		self.id = self.extract_id(url_id)
		self.mode = mode
		self.method = method
		self.min_date = min_date
		###############################
		# Init the video informations #
		###############################
		self.url	 = ""
		self.url_channel = ""
		self.title	 = ""
		self.location	 = ""
		self.date	 = ""
		self.data_file	 = ""
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

	def add_sub(self, url):
		""" This function return the informations wich are write in sub.swy ."""
		sub = self.extract_id(url)
		name = re.findall('(.+?)-[0-9]*$', sub)[0].replace('-', ' ')
		return sub + '\t' + name

	def write(self):
		return self.file.write(
			url=self.url,
			title=self.title,
			url_img='https://www.dailydot.com/wp-content/uploads/558/89/tdd-classical_music_emojis.jpg',
			channel=self.location,
			date=self.date,
			data_file=self.data_file)

	def info_html(self, ele):
			self.date		= re.findall(r'<time itemprop="startDate" datetime="(.+?)"', ele)[0].split('T')[0].replace('-', '/')
			self.data_file	= [self.date.replace('/', ''), '000000']
			self.url		= 'https://www.infoconcert.com' + re.findall(r'itemprop="url"\n.*href="(.+?)"', ele)[0]
			self.location	= re.findall(r'<span itemprop="name">(.+?)</span>', ele)[0]
			self.location	+= ' - ' + re.findall(r'<span itemprop="locality">(.+?)</span>', ele)[0]
			raw_singers		= re.findall('<div class="spectacle">(.+?)</div>', ele, re.DOTALL)[0]
			singers			= re.findall('>(.+?)</a>', raw_singers)
			i = False
			self.title		= ""
			for singer in singers:
				if i:
					self.title += '/'
				i = True
				self.title += singer

	def analyzer_sub(self):
		""" The main function wich retrieve the informations and and write it
		in a file"""
		data = download_html_infoconcert(self.id)
		if data == None:
			return
		for ele in data:
			self.info_html(ele)
			self.write()

	def old(self, url, lcl):
		""" The function wich is call with the option -o
		This function print the old channel or the dead channel."""

	def dead(self, url):
		""" The function wich is call with the option -d
		This function print the dead channel."""

	def stat(self, sub, name):
		""" The function wich is call with the option -s
		This function print the views and the ratio of like of a video"""

