from ..core.sock import download_https
from ..core.tools import log


def ptube_crtlink(info, type_file):
	if len(info) == 2 and info[1] != '':
		return '/feeds/videos.{}?accountId={}'.format(type_file, info[1])
	return '/feeds/videos.{}'.format(type_file)


def download_xml_peertube(url_id, split=True):
	info = url_id.split(':')
	site = download_https(ptube_crtlink(info, 'xml'), info[0])
	if site.status != '200':
		site = download_https(ptube_crtlink(info, 'xml').replace('accountId', 'videoChannelId'), info[0])
		if site.status != '200':
			log.Error('Failed to download ({})'.format(info))
			return None
	data = site.body
	if split:
		linfo = data.split('<item>')
		del linfo[0]
		if linfo == []:
			return None
		return linfo
	else:
		return data
