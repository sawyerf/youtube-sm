import socket
import ssl
import re
from time import time
from .tools import print_debug

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
			print_debug('Error Recv: {}'.format(e), 1)
			break
		if time() - trun > TIMEOUT or raw_data == b'':
			break
		data += raw_data
	sock.close()
	try:
		data = data.decode('utf8')
		if not re.match(r'HTTP/1\.[0-1] 200', data):
			print_debug("Error: {} ({})".format(data.split('\r\n')[0], url), 1)
			return None
		return data
	except:
		print_debug('Can\'t decode data recv ({})'.format(url), 1)
		return None

def download_http(url, host='youtube.com'):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, 80))
	sock.settimeout(1);
	sock.send(b"GET " + url + b" HTTP/1.0\r\nHost: www." + host.encode() + b"\r\n\r\n")
	return recv(sock, host + url.decode())

def download_https(url, host='youtube.com'):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	context = ssl._create_default_https_context()
	context.check_hostname = host
	sock = context.wrap_socket(sock, server_hostname=host)
	try:
		sock.connect((host, 443))
	except Exception as e:
		print_debug('{} ({}{})'.format(e, host, url), 1)
		return None
	sock.settimeout(1);
	sock.write(b"GET " + url + b' HTTP/1.1\r\nHost: www.' + host.encode() + b'\r\nAccept-Language: en\r\n\r\n')
	return recv(sock, 'https://' + host + url.decode())
