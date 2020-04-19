import re
from threading		import Thread
from .analyzer		import Analyzer
from ..core.tools	import (
	log
)
from ..downloader.revolutionpermanente	import (
	download_xml_revolutionpermanente
)

class RevolutionPermanente_Analyzer(Thread, Analyzer):
	SITE='[revolutionpermanente]'
	URL_MATCH=r'(?:https://|)(?:www\.|)revolutionpermanente\.fr.*'

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
		self.title		= ''
		self.url		= ''
		self.url_img	= ''
		self.data_file	= ''
		self.date		= ''
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
		return 'Revolution Permanente'

	def write(self):
		return self.file.write(
			url=self.url,
			title=self.title,
			url_img=self.url_img,
			channel='Revolution Permanente',
			url_channel='https://www.revolutionpermanente.fr/',
			date=self.date,
			data_file=self.data_file
		)

	def info_rss(self, ele):
			self.title = re.findall('<title>(.*)</title>', ele)[0]
			self.url = re.findall('<link>(.*)</link>', ele)[0]
			self.url_img = re.findall("img class='spip_logo spip_logo_right spip_logos' .* src='(.+?)'", ele)[0]
			date = re.findall('<dc:date>(.*)</dc:date>', ele)[0].replace('Z', '').split('T')
			self.data_file = [date[0].replace('-', ''), date[1].replace(':', '')]
			self.date = date[0]

	def analyzer_sub(self):
		""" The main function wich retrieve the informations and and write it
		in a file"""
		data = download_xml_revolutionpermanente()
		if data == None:
			return
		for ele in data:
			self.info_rss(ele)
			self.write()

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
