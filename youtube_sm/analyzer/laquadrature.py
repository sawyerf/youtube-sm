from .analyzer    import Analyzer
from ..downloader.laquadrature import download_rss_quadrature
import re

class LaQuadrature_Analyzer(Analyzer):
	SITE='[laquadrature]'
	LANG_MATCH=r'fr|en|es'
	URL_MATCH=r'(?:https://|)(?:www\.|)laquadrature\.net(?:/(?P<ID>%s)|)' % LANG_MATCH
	TEST=[
		'laquadrature.net/fr',
		'https://laquadrature.net/',
		'https://www.laquadrature.net/en',
		'www.laquadrature.net/es',
		'fr',
		'en',
		'es',
	]

	def __init__(self, url_id=''):
		######################
		# The basic variable #
		######################
		self.id = self.extract_id(url_id)
		###############################
		# Init the video informations #
		###############################
		self.content = {}

	def extract_id(self, url):
		match = re.match(self.URL_MATCH, url)
		if not match:
			if re.match(r'(%s)$' % self.LANG_MATCH, url):
				return url
			return None
		lang = match.group('ID')
		if lang is not None and re.match(r'(%s)$' % self.LANG_MATCH, lang):
			return lang
		return 'fr'

	def add_sub(self, sub):
		""" This function return the informations wich are write in sub.swy ."""
		lang = self.extract_id(sub)
		if lang is None:
			return None
		return lang + '\t' + 'la quadrature du net'

	def real_analyzer(self):
		""" The main function  wich retrieve the informations and and write it
		in a file"""
		datas = download_rss_quadrature(self.id)
		if datas is None:
			return
		for data in datas:
			content = self.info(data, {
				'url': {'re': '<link>(.+?)</link>'},
				'title': {'re': '<title>(.+?)</title>'},
				'url_uploader': {'default': 'https://www.laquadrature.net/' + self.id},
				'image': {'default': 'https://static.mediapart.fr/etmagine/default/files/media_275614/la_quadrature.png'},
				'uploader': {'default': 'La Quadrature du Net'},
				'date': {'re': '<pubDate>(.+?) \+0000</pubDate>', 'date': '%a, %d %b %Y %H:%M:%S'},
			})
			if content is not None:
				self.file.add(**content)

	def old(self, url, lcl):
		""" The function wich is call with the option -o
		This function print the old channel or the dead channel."""

	def dead(self, url):
		""" The function wich is call with the option -d
		This function print the dead channel."""
