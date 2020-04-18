from ..core.sock	import download_https


def download_xml_daily(url_id, split=True):
	data = download_https('/rss/user/' + url_id, 'www.dailymotion.com')
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

