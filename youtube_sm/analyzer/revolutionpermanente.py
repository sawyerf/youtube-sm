import re
from datetime		import datetime
from threading		import Thread
from .analyzer		import Analyzer
from ..core.tools	import (
	log
)
from ..downloader.revolutionpermanente	import (
	download_xml_revolutionpermanente
)

class RevolutionPermanente_Analyzer(Analyzer):
	SITE='[revolutionpermanente]'
	URL_MATCH=r'(?:https://|)(?:www\.|)revolutionpermanente\.fr.*'

	def __init__(self, url_id='', mode='', method='0', file=None, prog=None):
		######################
		# The basic variable #
		######################
		self.id = url_id
		self.mode = mode
		self.method = method
		###############################
		# Init the video informations #
		###############################
		self.title		= ''
		self.url		= ''
		self.url_img	= ''
		self.date		= ''
		################
		# The function #
		################
		self.prog = prog
		self.file = file

	def add_sub(self, url):
		""" This function return the informations wich are write in sub.swy ."""
		return 'Revolution Permanente'

	def write(self):
		return self.file.add(
			url=self.url,
			title=self.title,
			image=self.url_img,
			uploader='Revolution Permanente',
			url_uploader='https://www.revolutionpermanente.fr/',
			date=self.date,
		)

	def info_rss(self, ele):
			self.title		= re.findall('<title>(.*)</title>', ele)[0]
			self.url		= re.findall('<link>(.*)</link>', ele)[0]
			self.url_img	= re.findall("img class='spip_logo spip_logo_right spip_logos' .* src='(.+?)'", ele)[0]
			date			= re.findall('<dc:date>(.*)</dc:date>', ele)[0]
			self.date		= datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')

	def real_analyzer(self):
		""" The main function wich retrieve the informations and and write it
		in a file"""
		data = download_xml_revolutionpermanente()
		if data == None:
			return
		for ele in data:
			try:
				self.info_rss(ele)
			except:
				pass
			self.write()
