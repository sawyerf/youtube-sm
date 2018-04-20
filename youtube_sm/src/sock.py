import socket
import ssl
import time

def download_page(url_id, type_id=True, split=True, method='0'):
	if method == '0':
		return download_xml(url_id, type_id, split)
	elif method == '1':
		return download_html(url_id, type_id, split)
	else:
		return None

def download_xml(url_id, type_id=True, split=True):
	"""Return a list of informations of each video with the 
	RSS youtube page"""
	nb = 0
	data = b""
	if type_id: #Channel
		url = b'/feeds/videos.xml?channel_id=' + url_id.encode()
	else: #Playlist
		url = b'/feeds/videos.xml?playlist_id=' + url_id.encode()
	data = download_http(url)
	if split:
		linfo = data.split("<entry>")
		del linfo[0]
		if linfo == []:
			return None
		return linfo
	else:
		return data

def download_html(url_id, type_id=True, split=True):
	"""Return a list of informations of each video with the
	current html page"""
	if type_id:
		url = b'/channel/' + url_id.encode() + b'/videos'
	else:
		url = b'/playlist?list=' + url_id.encode()
	data = download_https(url)
	if data == None:
		return None
	if split:
		if type_id: #channel
			linfo = data.split('<div class="yt-lockup-content">')
			if len(linfo) <= 1:
				return None
		else: #playlist
			linfo = data.split('<tr class="pl-video yt-uix-tile "')
			del linfo[0]
			if linfo == []:
				return None
		return linfo
	else:
		return data

def download_http(url):
	data = b''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("youtube.com", 80))
	sock.send(b"GET " + url + b" HTTP/1.0\r\nHost: www.youtube.com\r\n\r\n")
	while True:
		raw_data = sock.recv(1024)
		if raw_data == b"":
			break
		else:
			data += raw_data
	sock.close()
	try:
		return data.decode('utf8')
	except:
		return None

def download_https(url):
	data = b''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("youtube.com", 443))
	for i in range(5):
		try:
			ssock = ssl.wrap_socket(sock)
		except OSError:
			time.sleep(1)
			if i == 4:
				return None
		else:
			break
	ssock.write(b"GET " + url + b' HTTP/1.1\r\nHost: www.youtube.com\r\nAccept-Language: en\r\n\r\n')
	# Recv the HTML page :
	while True:
		try:
			raw_data = ssock.recv(1000)
		except ConnectionResetError:
			return None
		except:
			break
		data += raw_data
		if b'</html>' in data[-20:] or raw_data == b'':
			break
	ssock.close()
	try:
		return data.decode('utf8')
	except:
		return None
