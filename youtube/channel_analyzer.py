from youtube.time import *
from youtube.analyzer import xml_recup
from threading import Thread

def old(url_data, min_tps=12):
	lcl = lcl_time(min_tps)
	threads = []
	for url in url_data:
		thr = Thread(target=thread_old, args=(url, lcl,))
		threads.append(thr)
		thr.start()
	for i in threads:
		i.join()

def thread_old(url, lcl):
	linfo = xml_recup(url)
	if linfo == False:
		print('[channel dead]', url)
	elif linfo == None:
		print('[  no video  ]', url)
	else:
		tps_vd = linfo[0].split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', '')
		if lcl > int(tps_vd):
			try:
				print('[ ' + tps_vd[:4] + '/' + tps_vd[4:6] + '/' + tps_vd[6:8] + ' ] ' + linfo[0].split('<name>')[1].split('</name>')[0])
			except UnicodeEncodeError:
				print('[ ' + tps_vd[:4] + '/' + tps_vd[4:6] + '/' + tps_vd[6:8] + ' ]', linfo[0].split('<name>')[1].split('</name>')[0].encode())
			except:
				print("[   erreur   ]", url)

def dead(url_data):
	threads = []
	for url in url_data:
		thr = Thread(target=thread_dead, args=(url,))
		threads.append(thr)
		thr.start()
	for i in threads:
		i.join()

def thread_dead(url):
		linfo = xml_recup(url)
		if linfo == False:
			print('[channel dead]\t', url)
		elif linfo == None:
			print('[  no video  ]\t', url)
