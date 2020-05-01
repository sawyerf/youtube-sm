import re

from datetime import datetime
from .analyzer import Analyzer
from ..downloader.revolutionpermanente import download_xml_revolutionpermanente


class RevolutionPermanente_Analyzer(Analyzer):
	SITE='[revolutionpermanente]'
	URL_MATCH=r'(?:https://|)(?:www\.|)revolutionpermanente\.fr.*'

	def __init__(self, url_id='', method='0', file=None, prog=None):
		######################
		# The basic variable #
		######################
		self.id = url_id
		self.method = method
		###############################
		# Init the video informations #
		###############################
		self.title   = ''
		self.url     = ''
		self.url_img = ''
		self.date    = ''
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


	def real_analyzer(self):
		""" The main function wich retrieve the informations and and write it
		in a file"""
		data = download_xml_revolutionpermanente()
		if data is None:
			return
		for ele in data:
			self.content = self.info(ele, {
				'title':{'re':'<title>(.*)</title>'},
				'url':{'re':'<link>(.*)</link>'},
				'url_img':{'re':"img class='spip_logo spip_logo_right spip_logos' .* src='(.+?)'"},
				'date':{'re':'<dc:date>(.*)</dc:date>','date':'%Y-%m-%dT%H:%M:%SZ'},
			})
			if self.content is not None:
				self.write()
