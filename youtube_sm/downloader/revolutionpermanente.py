from ..core.sock	import download_https
from ..core.tools import (
	log)

import re

def download_xml_revolutionpermanente(split=True):
	data = download_https('/spip.php?page=backend', 'www.revolutionpermanente.fr')
	if data == None:
			return None
	if split:
			linfo = re.findall('<item xml:lang="fr">(.+?)</item>', data, re.DOTALL)
			if linfo == []:
					return None
			return linfo
	return data
