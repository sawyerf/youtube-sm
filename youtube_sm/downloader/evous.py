import re
from ..core.sock import download_https


def download_html_evous(split=True):
	site = download_https("www.evous.fr", "/Les-Manifestations-a-Paris-la-semaine-1176044.html")
	if site.status != '200':
		return None
	data = site.body
	if split:
			linfo = re.findall('<br\ \/>-&nbsp;(<strong>.+?)\n', data, re.DOTALL)
			if linfo == []:
					return None
			return linfo
	return data
