from youtube.time import *
from youtube.analyzer import xml_recup

def old(url_data, min_tps=12):
	lcl = lcl_time(min_tps)
	for url in url_data:
		linfo = xml_recup(url)
		if linfo == False:
			print('[channel dead]\t', url)
		elif linfo == None:
			print('[  no video  ]\t', url)
		else:
			tps_vd = linfo[0].split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', '')
			if lcl > int(tps_vd):
				print('[ ' + tps_vd[:4] + '/' + tps_vd[4:6] + '/' + tps_vd[6:8] + ' ]\t', linfo[0].split('<name>')[1].split('</name>')[0])

def dead(url_data):
	for url in url_data:
		linfo = xml_recup(url)
		if linfo == False:
			print('[channel dead]\t', url)
		elif linfo == None:
			print('[  no video  ]\t', url)
