from ..core.sock import download_https
from ..core.tools import log


def download_xml_peertube(url_id):
	info = url_id.split(':')
	path = '/feeds/videos.xml'
	if len(info) == 2 and info[1] != '':
		path += '?accountId=' + info[1]

	site = download_https(info[0], path)
	if site.status != '200':
		site = download_https(info[0], path.replace('accountId', 'videoChannelId'))
		if site.status != '200':
			log.Error('Failed to download ({})'.format(info))
			return None
	data = site.body.split('<item>')
	del data[0]
	return data
