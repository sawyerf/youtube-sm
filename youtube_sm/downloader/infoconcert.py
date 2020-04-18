import re

from ..core.tools	import (
	log)
from ..core.sock	import (
	download_https
)

def download_html_infoconcert(gid):
	data = download_https('/artiste/{}/concerts.html'.format(gid), 'www.infoconcert.com')
	if data == None:
		return None
	data = data.split('id="artiste-tab-archives"')[0]
	sdat = data.split('panel panel-default date-line date-line-festival')
	del sdat[0]
	if sdat == []:
		return None
	return sdat
