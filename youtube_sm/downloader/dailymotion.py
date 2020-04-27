from ..core.sock import download_https


def download_xml_daily(url_id, split=True):
	site = download_https('/rss/user/' + url_id, 'www.dailymotion.com')
	if site.status != '200':
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
