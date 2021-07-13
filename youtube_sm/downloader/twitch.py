import re
import json

from ..core.sock import download_https


def download_twitch(sid):
	site = download_https('www.twitch.tv', '/{}/videos?filter=all'.format(sid))
	if site.status != '200':
		return None
	data = re.findall('<script type="application/ld\+json">(.+?)</script>', site.body)
	if data == []:
		return None
	return json.loads(data[0])
