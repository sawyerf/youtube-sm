import re

from datetime  import datetime
from .analyzer import Analyzer
from ..downloader.infoconcert import (
	download_html_infoconcert
)
from ..core.tools import log


class InfoConcert_Analyzer(Analyzer):
	SITE='[infoconcert]'
	URL_MATCH=r'(?:https://|)(?:www\.|)infoconcert\.com/artiste/(?P<ID>[a-z0-9-]*-[0-9]*)'
	TEST=[
		'https://www.infoconcert.com/artiste/achab-175740/concerts.html',
		'https://www.infoconcert.com/artiste/pomme-139757/concerts.html',
		'achab-175740',
		'pomme-139757',
	]

	def __init__(self, url_id=''):
		######################
		# The basic variable #
		######################
		self.id = self.extract_id(url_id)
		###############################
		# Init the video informations #
		###############################
		self.channel = ''
		self.date = ''
		self.title = ''
		self.url = ''
		self.url_img = ''

	def add_sub(self, url):
		""" This function return the informations wich are write in sub.swy ."""
		sub = self.extract_id(url)
		name = re.findall('(.+?)-[0-9]*$', sub)[0].replace('-', ' ')
		return sub + '\t' + name

	def write(self):
		return self.file.add(
			url=self.url,
			title=self.title,
			image='https://www.dailydot.com/wp-content/uploads/558/89/tdd-classical_music_emojis.jpg',
			uploader=self.location,
			date=self.date,
		)

	def info_html(self, ele):
		date          = re.findall(r'<time itemprop="startDate" datetime="(.+?)"', ele)[0]
		self.date     = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
		self.url      = 'https://www.infoconcert.com' + re.findall(r'itemprop="url"\n.*href="(.+?)"', ele)[0]
		self.location = re.findall(r'<span itemprop="name">(.+?)</span>', ele)[0]
		self.location += ' - ' + re.findall(r'<span itemprop="locality">(.+?)</span>', ele)[0]
		raw_singers   = re.findall('<div class="spectacle" >(.+?)</div>', ele, re.DOTALL)[0]
		singers       = re.findall('>(.+?)</a>', raw_singers)
		self.title    = '/'.join(singers)

	def real_analyzer(self):
		""" The main function wich retrieve the informations and and write it
		in a file"""
		data = download_html_infoconcert(self.id)
		if data is None:
			return
		for ele in data:
			try:
				self.info_html(ele)
				self.write()
			except:
				log.Warning('Fail To Parse the content of ({})'.format(self.id))

	def old(self, url, lcl):
		""" The function wich is call with the option -o
		This function print the old channel or the dead channel."""

	def dead(self, url):
		""" The function wich is call with the option -d
		This function print the dead channel."""
