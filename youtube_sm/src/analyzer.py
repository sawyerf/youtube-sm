import os
import time
import socket
from threading import Thread

def xml_recup(url):
	"""Return a list of informations of each video"""
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

def html_init(path):
	"""To init the html file"""
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

def init(urls, min_date, path='', mode='html'):
	threads = []
	for url in urls:
		thr = Analyzer(mode, url, min_date, path)
		thr.Thread()
		threads.append(thr)
		thr.start()
	for i in threads:
		i.join()

class Analyzer(Thread):
	"""It's a group of fonctions to recup the videos informations"""
	def __init__(self, mode='', url='', min_date='', path=''):
		self.mode = mode
		self.url = url
		self.path_cache = path
		self.min_date = min_date
		#all the var user in class
		self.url_channel = ""
		self.title = ""
		self.channel = ""
		self.date = []
		self.image = ""

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()

	def analyzer_sub(self):
		linfo = xml_recup(self.url)
		nb_new = 0
		if linfo == False or linfo == None:
			return 0
		for i in linfo:
			date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
			if self.min_date <= date:
				dvid = self.info_recup(i)
				if dvid:
					nb_new += 1
				else:
					return 0

	def info_recup(self, i):
		self.url = i.split('<yt:videoId>')[1].split('</yt:videoId>')[0]
		self.url_channel = i.split('<yt:channelId>')[1].split('</yt:channelId>')[0]
		self.title = i.split('<media:title>')[1].split('</media:title>')[0]
		self.channel = i.split('<name>')[1].split('</name>')[0]
		self.date = i.split('<published>')[1].split('+')[0].split('T')
		self.image = 'https://i.ytimg.com/vi/' + self.url  + '/mqdefault.jpg'
		if self.mode == 'html':
			return self.generate_data_html()
		elif self.mode == 'raw':
			return self.append_raw()
		elif self.mode == 'list':
			return self.append_list()

	def append_raw(self):
		open('sub_raw', 'a', encoding='utf8').write(self.date[0] + '\t' + self.url + '\t' + self.url_channel + '\t' + self.title + '\t' + self.channel + '\t' + self.image + '\n')
		return True

	def append_list(self):
		open('sub_list', 'a', encoding='utf8').write(self.date[0] + ' https://www.youtube.com/watch?v=' + self.url + '\n')
		return True

	def generate_data_html(self):
		try:
			data = open(self.path_cache + 'data/' + self.date[0] + '/' + self.date[1].replace(':', ''), 'rb+').read().decode("utf8")
			if self.url in data:
				return False
		except:
			try:
				os.mkdir(self.path_cache + 'data/' + self.date[0])
			except:
				pass
		open(self.path_cache + 'data/' + self.date[0] + '/' + self.date[1].replace(':', ''), 'a', encoding='utf-8').write("""<!--NEXT -->
	<div class="video">
		<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="{}" ></a>
		<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
		<a href="https://www.youtube.com/channel/{}"> <p>{}</p> </a>
		<p>{}</p>
		<p class="clear"></p>
	</div>
	""".format(self.url, self.image, self.url, self.title, self.url_channel, self.channel, self.date[0]))
		return True

def html_end(count=7, path=''):
	fch = sorted(os.listdir(path + 'data/'))
	if len(fch) < count:
		count = len(fch)
	elif count == -1:
		count = len(fch)
	for i in range(count):
		fch_in = sorted(os.listdir(path + 'data/' + fch[-1-i]))
		for a in range(len(fch_in)):
			data = open(path + 'data/' + fch[-1-i] + '/' + fch_in[-1-a], 'r', encoding='utf-8').read()
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
