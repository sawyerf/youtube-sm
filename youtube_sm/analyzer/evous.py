import re
import locale

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
		for i in infos:
			self.content = self.info(i, {
				'url': {'re':'<a href="(.*)" class'},
				'title': {'re':'<strong>(.*)</strong>'},
				'url_uploader': {'default':'https://www.evous.fr/Les-Manifestations-a-Paris-la-semaine-1176044.html'},
				'uploader': {'default':'Evous'},
				'image': {'default':"http://img.over-blog-kiwi.com/1/49/25/24/20160318/ob_bac2c2_code19.jpg"},
				'date': {'re':'</strong> le (\w* \d{1,2} \w* \d{4})', 'date':'%A %d %B %Y'},
			})
			if self.content is not None:
				self.file.add(**self.content)
		locale.setlocale(locale.LC_ALL, loc)
