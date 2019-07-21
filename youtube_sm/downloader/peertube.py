from ..src.sock	import download_https
from ..src.tools import (
	print_debug)

def ptube_crtlink(info, type_file):
	if len(info) == 2 and info[1] != '':
		return '/feeds/videos.{}?accountId={}'.format(type_file, info[1])
	return '/feeds/videos.{}'.format(type_file)

def	download_xml_peertube(url_id, split=True):
	info = url_id.split(':')
	data = download_https(ptube_crtlink(info, 'xml').encode(), info[0])
	if data == None:
		data = download_https(ptube_crtlink(info, 'xml').replace('accountId', 'videoChannelId').encode(), info[0])
		if data == None:
			print_debug('[!] Failed to download ({})'.format(info))
			return None
	if split:
		linfo = data.split('<item>')
		del linfo[0]
		if linfo == []:
			return None
		return linfo
	else:
		return data

def	download_atom_peertube(url_id, split=True):
	info = sub.split(':')
	data = download_https(ptube_crtlink(info, 'atom').encode(), info[0])
	if data == None:
		return None
	if split:
		linfo = data.split('<item>')
		del linfo[0]
		if linfo == []:
			return None
		return linfo
	else:
		return data
