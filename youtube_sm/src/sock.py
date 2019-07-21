import socket
import ssl
import time
from .tools import print_debug

def download_http(url, host='youtube.com'):
	data = b''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, 80))
	sock.send(b"GET " + url + b" HTTP/1.0\r\nHost: www." + host.encode() + b"\r\n\r\n")
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
		print_debug('[!] Can\'t decode data recv ({}{})'.format(host, url))
		return None

def download_https(url, host='youtube.com'):
	data = b''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, 443))
	sock.settimeout(1);
	for i in range(5):
		try:
			ssock = ssl.wrap_socket(sock)
		except OSError:
			time.sleep(1)
			if i == 4:
				print_debug('[!] Can\'t start the ssl connection ({}{})'.format(host, url))
				return None
		else:
			break
	ssock.write(b"GET " + url + b' HTTP/1.1\r\nHost: www.' + host.encode() + b'\r\nAccept-Language: en\r\n\r\n')
	# Recv the HTML page :
	while True:
		try:
			raw_data = ssock.recv(1000)
		except ConnectionResetError:
			print_debug('[!] Connection losted ({}{})'.format(host, url))
			return None
		except:
			break
		data += raw_data
		if b'\r\n0\r\n\r\n' in data[-20:] or raw_data == b'' or b'</rss>' in data[-20:] or b'</html>' in data[-20:]:
			break
		if b'200' not in data[:20]:
			print_debug("[!] {} (https://{}{})".format(data.decode().split('\r\n')[0], host, url.decode()))
			return None
	ssock.close()
	try:
		return data.decode('utf8')
	except:
		print_debug('[!] Can\'t decode data recv ({}{})'.format(host, url))
		return None
