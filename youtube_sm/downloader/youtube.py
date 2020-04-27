import re

from ..core.tools import log
from ..core.sock  import (
	download_http,
	download_https
)


def download_page(url_id, type_id=True, split=True, method='0'):
	if method == '0':
		return download_xml(url_id, type_id, split)
	elif method == '1':
		return download_html(url_id, type_id, split)
	else:
		return None


def download_xml(url_id, type_id=True, split=True):
	"""
	Return a list of informations of each video with the
	RSS youtube page
	"""
	if type_id:  # Channel
		url = '/feeds/videos.xml?channel_id=' + url_id
	else:  # Playlist
		url = '/feeds/videos.xml?playlist_id=' + url_id
	site = download_http(url)
	if site.status != '200':
		return None
	data = site.body
	if split:
		linfo = data.split("<entry>")
		del linfo[0]
		if linfo == []:
			log.Warning('No videos ({})'.format(url_id))
			return None
		return linfo
	else:
		return data


def download_html(url_id, type_id=True, split=True):
	"""
	Return a list of informations of each video with the
	current html page
	"""
	if type_id:
		url = '/channel/' + url_id + '/videos'
	else:
		url = '/playlist?list=' + url_id
		site = download_https(url)
		if site.status != '200':
			return None
		data = site.body
		url = data.split('<a href="/watch?v')[1].split('"')[0]
		url = '/watch?v' + url
	site = download_https(url)
	if site.status != '200':
		return None
	data = site.body
	if split:
		if type_id:  # Channel
			linfo = data.split('<div class="yt-lockup-content">')
			if len(linfo) <= 1:
				log.Warning('No videos ({})'.format(url_id))
				return None
		else:  # Playlist
			linfo = data.split('<li class="yt-uix-scroller-scroll-unit  vve-check"')
			del linfo[0]
			if linfo == []:
				log.Warning('No videos ({})'.format(url_id))
				return None
		return linfo
	else:
		return data


def download_html_playlist(url_id, split=True):
	"""
	Download the html page of a playlist and
	return the data, the next link to download and the size of the playlist
	"""
	data = download_html(url_id, False, False)
	try:
		len_play = int(re.findall(r'<span id="playlist-length">(.+?)videos</span>', data)[0])
	except:
		log.Warning("No video in this page ({})".format(url_id))
		return None, None, None
	linfo = data.split('<li class="yt-uix-scroller-scroll-unit  vve-check"')
	del linfo[0]
	if linfo == []:
		log.Warning("No video in this page ({})".format(url_id))
		return None, None, None
	try:
		next_link = '/watch?v=' + re.findall(r'<a href="/watch\?v=(.+?)"', linfo[-1])[0]
	except:
		next_link = None
	return linfo, next_link, len_play


def download_show_more(url, type_id=True):
	"""
	Download the page for the method 'ultra-html'
	and return the data and the next link to download
	"""
	if type_id:
		site = download_https(url)
		data = data.replace('\\n', '\n').replace('\\"', '"')
		if site.status != '200':
			return None
		data = site.body
		try:
			next_link = data.split('data-uix-load-more-href="\\')[1].split('"')[0]
		except:
			next_link = None
		data = data.split('yt-lockup-content')
		del data[0]
		return data, next_link
	else:
		site = download_https(url)
		if site.status != '200':
			return None
		data = site.body
		linfo = data.split('<li class="yt-uix-scroller-scroll-unit  vve-check"')
		del linfo[0]
		try:
			next_link = '/watch?v=' + re.findall(r'<a href="/watch\?v=(.+?)"', linfo[-1])[0]
		except:
			return None, None
		return linfo, next_link
