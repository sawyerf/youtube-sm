import re
from ..core.sock import download_https


def download_html_evous(split=True):
	site = download_https("www.evous.fr", "/Les-Manifestations-a-Paris-la-semaine-1176044.html")
	if site.status != '200':
		return None
	data = site.body
	if split:
			linfo = re.finditer('<strong>(?P<date>[A-Za-z]+? [0-9]+? [a-z]+? [0-9]{4})<\/strong>\n(?P<manifs>.+?)<p class="land-see-hero-caption', data, re.DOTALL)
			if linfo == []:
					return None
			return linfo
	return data
