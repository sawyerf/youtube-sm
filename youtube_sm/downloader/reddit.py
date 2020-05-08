import re

from ..core.sock import download_https


def download_rss_reddit(sid):
	site = download_https('www.reddit.com', '/{}/.rss'.format(sid))
	if site.status != '200':
		return None
	data = {}
	data['items'] = re.findall(r'<entry>(.+?)</entry>', site.body)
	title = re.findall(r'<title>(.+?)</title>', site.body)
	if title == []:
		return None
	data['title'] = title[0]
	return data
