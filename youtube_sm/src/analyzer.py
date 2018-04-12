import os
import time
import socket
import ssl
from threading import Thread

def type_id(id):
	"""True = Channel; False = Playlist"""
	if id[:2] == 'UC':
		return True
	elif id[:2] == 'PL':
		return False
	else:
		return True

def progress_bar(xmin, xmax):
	load = ''
	pc = (xmin/xmax)
	for i in range(int(pc*40)):
		load += '█'
	for i in range(int(40 - pc*40 + (pc*40)%1)):
		load += ' '
	print(str(pc*100)[:3] + ' %|' + load + '| ' + str(xmin) + ' analyzed', end='\r')
	if pc == 1:
		print()

def xml_recup(url, method=''):
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

def download_page(url_id, type_id=True):
	"""Return a list of informations of each video"""
	data = b''
	if type_id:
		url = b'GET /channel/' + url_id.encode() + b'/videos'
	else:
		url = b'GET /playlist?list=' + url_id.encode()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	ssock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1)
	ssock.connect(('youtube.com', 443))
	ssock.write(url + b' HTTP/1.0\r\nHost: www.youtube.com\r\n\r\n')
	while True:
		raw_data = ssock.recv(1000)
		data += raw_data
		if b'</html>' in data[-20:] or raw_data == b'':
			break
	ssock.close()
	data = data.decode('utf8')
	if type_id: #channel
		linfo = data.split('<div class="yt-lockup-content">')
	else: #playlist
		linfo = data.split('<div class="playlist-video-description">')
		del linfo[0]
		linfo[-1] = linfo[-1].split('<span class="vertical-align"></span>')[0]
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

def init(urls, min_date, path='', mode='html', loading=False, method=0):
	threads = []
	ending = 0
	for url in urls:
		thr = Analyzer(mode, url, min_date, method, path)
		thr.Thread()
		threads.append(thr)
		thr.start()
	for i in threads:
		i.join()
		ending += 1
		if loading:
			progress_bar(ending, len(threads))

class Analyzer(Thread):
	"""It's a group of fonctions to recup the videos informations"""
	def __init__(self, mode='', url_id='', min_date='', method=0, path=''):
		self.mode = mode
		# self.method is the way you're going to recv the data (0 -> RSS, 1 -> https://youtube.com/channel/{id}/videos) 
		self.method = method
		self.id = url_id
		self.path_cache = path
		self.min_date = min_date
		self.type = self._type_id()
		#all the var user in class
		self.url = ""
		self.url_channel = ""
		self.title = ""
		self.channel = ""
		self.date = []
		self.image = ""

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()

	def _type_id(self):
		return type_id(self.id)

	def _download_page(self):
		if self.method == 0:
			return xml_recup(self.id)
		elif self.method == 1:
			return download_page(self.id)
		else:
			return None

	def analyzer_sub(self):
		linfo = self._download_page()
		if linfo == False or linfo == None:
			return 0
		if self.method == 0:
			for i in linfo:
				date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
				if self.min_date <= date:
					dvid = self.info_recup(i)
		elif self.method == 1:
			self.channel = linfo[0].split('<title>')[1].split('\n')[0]
			del linfo[0]
			for i in linfo:
				lol = self.info_recup_html(i)
		else:
			return

	def date_process(self, raw_date):
		"""Return a conform date"""
		return raw_date.split(' ')

	def info_recup_html(self, i):
		"""Recup the informations of the html page"""
		if self.type: #Channel
			self.url = i.split('href="/watch?v=')[1].split('" rel')[0]
			self.url_channel = 'https://youtube.com/channel/{}'.format(self.id)
			self.title = i.split('dir="ltr" title="')[1].split('"')[0]
			self.date = self.date_process(i.split('</li><li>')[1].split('</li>')[0])
			self.image = 'https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url)
			return self.generate_data_html()
		else: #Playlist
			pass

	def info_recup_rss(self, i):
		"""Recup the informations of the rss page"""
		self.url = i.split('<yt:videoId>')[1].split('</yt:videoId>')[0]
		self.url_channel = i.split('<yt:channelId>')[1].split('</yt:channelId>')[0]
		self.title = i.split('<media:title>')[1].split('</media:title>')[0]
		self.channel = i.split('<name>')[1].split('</name>')[0]
		self.date = i.split('<published>')[1].split('+')[0].split('T')
		self.image = 'https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url)
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
	linfo = sorted(open('sub_raw', 'rb').read().decode('utf8').replace('\r', '').split('\n'))
	for i in range(len(linfo)):
		if linfo[i] == '':
			continue
		try:
			if linfo[-1-i][:10] != linfo[-2-i][:10]:
				nb += 1
				if nb == count:
					nb = i
					break
		except IndexError:
			break
		except:
			pass
	os.remove('sub_raw')
	time.sleep(0.01)
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
			try:
				if linfo[-1-i][:10] != linfo[-2-i][:10]:
					nb += 1
					if nb == count:
						nb = i
						break
			except IndexError:
				break
			except:
				pass
	os.remove('sub_list')
	fichier = open('sub_list', 'a', encoding='utf8')
	for i in range(nb):
		fichier.write(linfo[-1-i][11:] + '\n')
