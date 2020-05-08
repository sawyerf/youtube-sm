from ..core.sock import download_https


def download_html_infoconcert(gid):
	site = download_https('www.infoconcert.com', '/artiste/{}/concerts.html'.format(gid))
	if site.status != '200':
		return None
	data = site.body
	data = data.split('id="artiste-tab-archives"')[0]
	sdat = data.split('panel panel-default date-line date-line-festival')
	del sdat[0]
	if sdat == []:
		return None
	return sdat
