import re
from ..core.sock import download_https


def download_xml_revolutionpermanente(split=True):
	site = download_https('www.revolutionpermanente.fr', '/spip.php?page=backend')
	if site.status != '200':
		return None
	data = site.body
	if split:
			linfo = re.findall('<item xml:lang="fr">(.+?)</item>', data, re.DOTALL)
			if linfo == []:
					return None
			return linfo
	return data
