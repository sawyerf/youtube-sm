from ..core.sock import download_https
import re

def download_rss_quadrature(lang):
	url = '/%s/feed/' % lang
	if lang == 'fr':
		url = '/feed/'
	site = download_https('www.laquadrature.net', url)
	if site.status != '200':
		return None
	data = re.findall('<item>(.+?)</item>', site.body, re.DOTALL)
	return data
