import re

from datetime import datetime
from .analyzer import Analyzer
from ..downloader.revolutionpermanente import download_xml_revolutionpermanente


class RevolutionPermanente_Analyzer(Analyzer):
	SITE='[revolutionpermanente]'
	URL_MATCH=r'(?:https://|)(?:www\.|)revolutionpermanente\.fr.*'
	TEST=[
		'https://revolutionpermanente.fr/'
		'www.revolutionpermanente.fr/'
	]

	def __init__(self, url_id=''):
		self.id = url_id

	def add_sub(self, url):
		""" This function return the informations wich are write in sub.swy ."""
		return 'Revolution Permanente'

	def real_analyzer(self):
		""" The main function wich retrieve the informations and and write it
		in a file"""
		data = download_xml_revolutionpermanente()
		if data is None:
			return
		for ele in data:
			self.content = self.info(ele, {
				'url':{'re':'<link>(.*)</link>'},
				'title':{'re':'<title>(.*)</title>'},
				'url_uploader':{'default':'https://www.revolutionpermanente.fr/'},
				'uploader':{'default':'Revolution Permanente'},
				'image':{'re':"img class='spip_logo spip_logo_right spip_logos' .* src='(.+?)'"},
				'date':{'re':'<dc:date>(.*)</dc:date>','date':'%Y-%m-%dT%H:%M:%SZ'},
			})
			if self.content is not None:
				self.file.add(**self.content)
