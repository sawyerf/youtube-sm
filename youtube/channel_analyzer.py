from youtube.time import *
from youtube.html import xml_recup

def old(url_data):
	lcl = lcl_time(12)
	for url in url_data:
		linfo = xml_recup(url)
		if linfo == False:
			print(url, 'channel dead')
		else:
			tps_vd = int(linfo[0].split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
			if lcl > tps_vd:
				print(linfo[0].split('<name>')[1].split('</name>')[0], tps_vd)

def dead(url_data):
	for url in url_data:
		if xml_recup(url) == False:
			print(url)
