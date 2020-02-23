import socket
import ssl
import re
from time import time
from .tools import log

TIMEOUT = 2

def recv(sock, url):
	data = b""
	trun = time()
	while True:
		raw_data = b""
		try:
			raw_data = sock.recv(100000)
		except socket.timeout:
			if data != b'':
				break
		except Exception as e:
			log.warning('Error Recv: {}'.format(e))
			break
		if time() - trun > TIMEOUT or raw_data == b'':
			break
		data += raw_data
	sock.close()
	try:
		data = data.decode('utf8')
		if not re.match(r'HTTP/1\.[0-1] 200', data):
			log.error("Error: {} ({})".format(data.split('\r\n')[0], url))
			return None
		return data
	except:
		log.warning('Can\'t decode data recv ({})'.format(url))
		return None

def download_http(url, host='youtube.com'):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, 80))
	sock.settimeout(1);
	sock.send(b"GET " + url + b" HTTP/1.0\r\nHost: www." + host.encode() + b"\r\n\r\n")
	return recv(sock, host + url.decode())

def download_https(url, host='www.youtube.com'):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	context = ssl._create_default_https_context()
	context.check_hostname = host
	sock = context.wrap_socket(sock, server_hostname=host)
	try:
		sock.connect((host, 443))
	except Exception as e:
		log.error('{} ({}{})'.format(e, host, url))
		return None
	sock.settimeout(1);
	sock.write('GET {} HTTP/1.1\r\nHost:{}\r\nAccept-Language: en\r\n\r\n'.format(url, host).encode())
	return recv(sock, 'https://' + host + url)
