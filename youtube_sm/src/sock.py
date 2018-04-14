import socket
import ssl
import time

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
	# Init socket and SSL:
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
	ssock.write(url + b' HTTP/1.1\r\nHost: www.youtube.com\r\nAccept-Language: en\r\n\r\n')
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
	# Split :
	data = data.decode('utf8')
	if type_id: #channel
		linfo = data.split('<div class="yt-lockup-content">')
	else: #playlist
		linfo = data.split('<tr class="pl-video yt-uix-tile "')
		del linfo[0]
	return linfo
