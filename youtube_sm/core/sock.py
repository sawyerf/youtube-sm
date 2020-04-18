import socket
import ssl
import re
import zlib
from time import time
from .tools import log

TIMEOUT = 2

def recv(sock, url):
	data = b""
	trun = time()
	lenght = None
	while True:
		raw_data = b""
		try:
			raw_data = sock.recv(100000)
		except socket.timeout:
			if lenght != None and len(data) > lenght:
				break
		except Exception as e:
			log.Warning('Error Recv: {}'.format(e))
			break
		if lenght == None and ( b'Content-Length:' in data or b'content-length:' in data ):
			headers = data.split(b'\r\n\r\n')[0].decode()
			lenght = int(re.findall(r'[Cc]ontent-[Ll]ength: (.*)\r', headers)[0]) + len(headers)
		if time() - trun > TIMEOUT:
			break
		data += raw_data
	sock.close()
	try:
		data = data.decode('utf8')
		if not re.match(r'HTTP/1\.[0-1] 200', data):
			log.Warning("Error: {} ({})".format(data.split('\r\n')[0], url))
			return None
		return data
	except:
		if b'gzip' in data:
			body = data.split(b'\r\n\r\n')[1]
			try:
				body = zlib.decompress(body, 16+zlib.MAX_WBITS)
				return body.decode()
			except:
				log.Warning('Can\'t decode data recv ({})'.format(url))
				return None

def download_http(url, host='www.youtube.com'):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, 80))
	sock.settimeout(0.1);
	sock.send("""GET {} HTTP/1.1
Host:{}
Accept-Language: en
Accept: */*
Accept-Encoding: gzip, raw

""".format(url.decode(), host).replace('\n', '\r\n').encode())
	return recv(sock, host + url.decode())

def download_https(url, host='www.youtube.com'):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	context = ssl._create_default_https_context()
	context.check_hostname = host
	sock = context.wrap_socket(sock, server_hostname=host)
	try:
		sock.connect((host, 443))
	except Exception as e:
		log.Error('{} ({}{})'.format(e, host, url))
		return None
	sock.settimeout(0.1);
	sock.write("""GET {} HTTP/1.1
Host:{}
Accept-Language: en
Accept: */*
Accept-Encoding: raw

""".format(url, host).replace('\n', '\r\n').encode())
	return recv(sock, 'https://' + host + url)
