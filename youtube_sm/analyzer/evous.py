import re
import locale
from datetime  import datetime

from ..core.tools import log
from ..downloader.evous import download_html_evous
from .analyzer	import Analyzer

class Evous_Analyzer(Analyzer):
	SITE='[evous]'
	URL_MATCH=r'(?:https://|)(?:www\.|)evous\.fr(?:/.*|)'
	TEST=[
		'https://www.evous.fr/',
		'https://www.evous.fr/Les-Manifestations-a-Paris-la-semaine-1176044.html',
	]

	def __init__(self, url_id=''):
		pass

	def add_sub(self, sub):
		"""
		This function return the informations wich are write in sub.swy.
		"""
		return 'evous'

	def real_analyzer(self):
		"""
		The main function wich retrieve the informations and and write it
		in a file
		"""
		infos = download_html_evous()
		loc = locale.getlocale()
		try:
			locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
		except locale.Error as e:
			log.Error("Evous: ", e, ": You need to add `fr_FR.UTF-8`")
			return
		for day in infos:
			manifs = re.findall(r'(?:<br\ \/>.+?\n)', day.group('manifs'))
			dateManif = datetime.strptime(day.group('date'), '%A %d %B %Y')
			for manif in manifs:
				self.content = self.info(manif, {
					'url': {'re':'<a href="(.+?)" class', 'default': ''},
					'title': {'re':'<strong>(.+?)</strong>'},
					'url_uploader': {'default':'https://www.evous.fr/Les-Manifestations-a-Paris-la-semaine-1176044.html'},
					'uploader': {'default':'Evous'},
					'image': {'default':"http://img.over-blog-kiwi.com/1/49/25/24/20160318/ob_bac2c2_code19.jpg"},
					# 'date': {'re':'</strong> le (\w* \d{1,2} \w* \d{4})', 'date':'%A %d %B %Y', 'default': dateManif},
					'date': {'default': dateManif},
				})
				if self.content is not None:
					print(dateManif, self.content['title'])
					if re.match(r'<a .*>.+?</a>', self.content['title']):
						self.content['title'] = re.findall(r'<a .*>(.+?)</a>', self.content['title'])[0]
					if re.match(r'^/.*', self.content['url']):
						self.content['url'] = 'https://www.evous.fr' + self.content['url']
					self.file.add(**self.content)
		locale.setlocale(locale.LC_ALL, loc)
