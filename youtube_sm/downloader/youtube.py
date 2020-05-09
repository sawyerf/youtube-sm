import re

from ..core.tools import log
from ..core.sock  import (
	download_http,
	download_https
)

def download_xml(url_id, type_id=True, split=True):
	"""
	Return a list of informations of each video with the
	RSS youtube page
	"""
	if type_id:  # Channel
		url = '/feeds/videos.xml?channel_id=' + url_id
	else:  # Playlist
		url = '/feeds/videos.xml?playlist_id=' + url_id
	site = download_http('www.youtube.com', url)
	if site.status != '200':
		return None
	data = site.body
	if split:
		linfo = data.split("<entry>")
		del linfo[0]
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
		site = download_https('www.youtube.com', '/playlist?list=' + url_id, useragent='youtube-sm')
		if site.status != '200':
			return None
		url = re.findall('<a href="(/watch\?v.+?)"', site.body)
		if url == []:
			log.Error('Fail to parse html page')
			return None
		url = url[0]
	site = download_https('www.youtube.com', url, useragent='youtube-sm')
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
