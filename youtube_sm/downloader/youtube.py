import re
import json

from ..core.tools import log
from ..core.sock  import (
	download_http,
	download_https
)
from ..core.download  import Download

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
	site = Download(True, 'www.youtube.com')
	site.download(url, headers={'Cookie': 'CONSENT=YES+cb.20210413-13-p0.fr+FX+878', 'Referer': 'https://consent.youtube.com/'})
	if site.status != '200':
		return None
	data = site.body
	if split:
		if type_id:  # Channel
			lol = re.findall(">var ytInitialData = (\{.*});</script>", data)[0]
			#open('lol', 'w').write(lol)
			jso = json.loads(lol)
			return jso
	else:
		return data
