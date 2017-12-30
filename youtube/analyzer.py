import os 
import time
import socket
from threading import Thread


def html_init():
	try:
		os.mkdir('data')
	except:
		pass
	open('sub.html', 'w').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="css/sub.css" />
		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>
		<title>Abonnements</title>
	</head>
	<body>
<!-- {} -->
""".format(time.ctime()))

def init(url_data, min_date, mode='html'): 
	threads = []
	for url in url_data:
		thr = Thread(target=analyzer_sub, args=(url, min_date, mode,))
		threads.append(thr)
		thr.start()
	for i in threads:
		i.join()

def analyzer_sub(url, min_date, mode):
	linfo = xml_recup(url)
	nb_new = 0
	if linfo == False or linfo == None:
		return 0
	for i in linfo:
		date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
		if min_date <= date:
			dvid = info_recup(i, mode)
			if dvid:
				nb_new += 1
			else:
				return 0

def xml_recup(url):
	nb = 0
	data = b""
	if url[:2] == 'UC':
		url_xml = b'GET /feeds/videos.xml?channel_id=' + url.encode()
	elif url[:2] == 'PL':
		url_xml = b'GET /feeds/videos.xml?playlist_id=' + url.encode()
	else:
		return None
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("youtube.com", 80))
	sock.send(url_xml + b" HTTP/1.0\r\nHost: www.youtube.com\r\n\r\n")
	while True:
		raw_data = sock.recv(1024)
		if raw_data == b"":
			break
		else:
			data += raw_data
	sock.close()
	data = data.decode('utf8')
	linfo = data.split("<entry>")
	del linfo[0]
	if linfo == []:
		return None
	return linfo

def info_recup(i, mode):
	url = i.split('<yt:videoId>')[1].split('</yt:videoId>')[0]
	url_channel = i.split('<yt:channelId>')[1].split('</yt:channelId>')[0]
	title = i.split('<media:title>')[1].split('</media:title>')[0]
	channel = i.split('<name>')[1].split('</name>')[0]
	date = i.split('<published>')[1].split('+')[0].split('T')
	image = 'https://i.ytimg.com/vi/' + url  + '/mqdefault.jpg'
	if mode == 'html':
		return generate_data_html(url, url_channel, title, channel, date, image)
	elif mode == 'raw':
		open('sub_raw', 'a', encoding='utf8').write(date[0] + '\t' + url + '\t' + url_channel + '\t' + title + '\t' + channel + '\t' + image + '\n')
		return True
	elif mode == 'list':
		open('sub_list', 'a', encoding='utf8').write(date[0] + ' https://www.youtube.com/watch?v=' + url + '\n')
		return True

def generate_data_html(url, url_channel, title, channel, date, image):
	try:
		data = open('data/' + date[0] + '/' + date[1].replace(':', ''), 'rb+').read().decode("utf8")
		if url in data:
			return False
	except:
		try:
			os.mkdir('data/' + date[0])
		except:
			pass
	open('data/' + date[0] + '/' + date[1].replace(':', ''), 'a', encoding='utf-8').write("""<!--NEXT -->
<div class="video">
	<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="{}" ></a>
	<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
	<a href="https://www.youtube.com/channel/{}"> <p>{}</p> </a>
	<p>{}</p>
	<p class="clear"></p>
</div>
""".format(url, image, url, title, url_channel, channel, date[0]))
	return True

def html_end(count=7):
	fch = sorted(os.listdir('data/'))
	if len(fch) < count:
		count = len(fch)
	elif count == -1:
		count = len(fch)
	for i in range(count):
		fch_in = sorted(os.listdir('data/' + fch[-1-i]))
		for a in range(len(fch_in)):
			data = open('data/' + fch[-1-i] + '/' + fch_in[-1-a], 'r', encoding='utf-8').read()
			open('sub.html', 'a', encoding='utf-8').write(data)
	open('sub.html', 'a').write('</body></html>')

def raw_end(count=7):
	nb = 0
	linfo = sorted(open('sub_raw', 'r').read().split('\n'))
	for i in range(len(linfo)):
		if linfo[-1-i][:10] != linfo[-2-i][:10]:
			nb += 1
			if nb == count:
				nb = i
				break
	os.remove('sub_raw')
	fichier = open('sub_raw', 'a', encoding='utf8')
	for i in range(nb):
		fichier.write(linfo[-1-i] + '\n')

def list_end(count=7):
	nb = 0
	linfo = sorted(open('sub_list', 'r').read().split('\n'))
	if count == -1:
		nb = len(linfo)
	else:
		for i in range(len(linfo)):
			if linfo[-1-i][:10] != linfo[-2-i][:10]:
				nb += 1
				if nb == count:
					nb = i
					break
	os.remove('sub_list')
	fichier = open('sub_list', 'a', encoding='utf8')
	for i in range(nb):
		fichier.write(linfo[-1-i][11:] + '\n')
