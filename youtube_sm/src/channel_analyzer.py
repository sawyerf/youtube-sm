from .time import lcl_time
from .sock import download_xml
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
	""" Print the old channel """
	linfo = download_xml(url)
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
	""" Print the dead channel """
	linfo = download_xml(url)
	if linfo == False:
		print('[channel dead]\t', url)
	elif linfo == None:
		print('[  no video  ]\t', url)


def stats(subs):
	for sub in subs:
		threads = []
		thr = Thread(target=stat, args=(sub, subs[sub],))
		threads.append(thr)
		thr.start()
	for i in threads:
		i.join()


def stat(sub, name=''):
	"""Print the mark and the views of a channel"""
	data = download_xml(sub)
	if data == None or data == False:
		return
	marks = 0
	views = 0
	count_marks = 0
	for i in data:
		mark, view = recup_stats(i)
		if mark != None:
			marks += mark
			count_marks += 1
		views += view
	marks = marks / (count_marks / 2)
	prin = str(marks)[:4] + " for " + name + ' (' + str(views) + ' views)'
	try:
		print(prin)
	except:
		print(prin.encode())

def recup_stats(data):
	raw = data.split("<media:community>")[1].split("</media:community>")[0]
	try:
		mark = float(data.split("average=\"")[1].split("\"")[0])
	except:
		mark = None
	try:
		view = int(data.split("views=\"")[1].split("\"")[0])
	except:
		view = 0
	return mark, view
