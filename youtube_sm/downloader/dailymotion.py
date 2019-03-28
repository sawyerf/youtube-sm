from ..src.sock	import download_https
from ..src.tools import (
	print_debug)

def download_xml_daily(url_id, split=True):
	data = download_https(b'/rss/user/' + url_id.encode(), 'dailymotion.com')
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

