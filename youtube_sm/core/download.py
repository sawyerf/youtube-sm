from time   import time
from .tools import log

import socket
import ssl
import re
import zlib


class Download():
	LANGUAGE = 'en'
	SETTIMEOUT = 0.1
	TIMEOUT = 3
	USERAGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'
	def __init__(self, https, host):
		self.ssl  = https
		self.host = host
		self.setvar()

	def setvar(self):
		self.status   = ''
		self.headers  = ''
		self.body     = ''
		self.content_length = 0

	def create_request(self, url, method, body, headers):
		req = "{} {} HTTP/1.1\r\n".format(method, url)
		req += "Host: {}\r\n".format(self.host)

		default = {
			'User-Agent': self.USERAGENT,
			'Accept': '*/*',
			'Accept-Encoding': 'gzip',
			'Accept-Language': self.LANGUAGE
		}
		for key in default:
			if key not in headers:
				headers[key] = default[key]
		if body is not None:
			headers["Content-Length"] = str(len(body))
		for name in headers:
			req += '{}: {}\r\n'.format(name, headers[name])
		req += "\r\n"
		if body is not None:
			req += body
		return req.encode()

	def real_recv(self, sock):
		raw_data = b''
		try:
			raw_data = sock.recv(100000)
			return raw_data
		except socket.timeout:
			return b''
		except Exception as e:
			log.Error('Error Recv: {}'.format(e))
			return None

	def recv_headers(self, sock):
		data = b''
		trun = time()
		while True:
			data += self.real_recv(sock)
			if b'\r\n\r\n' in data:
				self.headers = data.split(b'\r\n\r\n')[0].decode()
				len_headers = len(self.headers) + 4
				self.status = re.findall(r'HTTP/1\.1 ([0-9]*)', self.headers)[0]
				if self.status != '100':
					return data[len_headers:]
				trun = time()
				data = data[len_headers:]
			elif time() - trun > self.TIMEOUT:
				self.headers = data.decode()
				return None

	def recv_body(self, sock, data, dlen):
		trun = time()
		while True:
			data += self.real_recv(sock)
			if ( dlen == -1 and time() - trun > self.TIMEOUT ) \
				or ( dlen != -1 and dlen <= len(data) ):
				self.body = data
				return

	def recv_chunk_body(self, sock, data):
		trun = time()
		dlen = 0
		data = b'\r\n' + data
		while True:
			data += self.real_recv(sock)
			while dlen < len(data) and b'\r\n' in data[dlen + 2:]:
				suite = data[dlen + 2:]
				if suite == b'':
					continue
				str_dlen = suite.split(b'\r\n')[0].decode()
				if not re.match('[0-9A-Fa-f]*$', str_dlen):
					log.Warning('Chunk recv failed')
					return self.recv_body(sock, data, -1)
				if int(str_dlen, 16) == 0:
					data = data[:dlen]
					self.body = data
					return
				len_dlen = len(str_dlen) + 2
				data = data[:dlen] + suite[len_dlen:]
				dlen += int(str_dlen, 16)

	def recv(self, sock, url):
		body = self.recv_headers(sock)
		if self.headers == '' or self.status == '204' or body is None:
			return
		if re.match('.*[Cc]ontent-[Ll]ength: .*', self.headers, re.DOTALL):
			dlen = int(re.findall('[Cc]ontent-[Ll]ength: (.*)\r', self.headers)[0])
			self.recv_body(sock, body, dlen)
		elif re.match('.*[Tt]ransfer-[Ee]ncoding:[ \t]*[Cc]hunked.*', self.headers, re.DOTALL):
			self.recv_chunk_body(sock, body)
			sock.settimeout(1)
		else:
			self.recv_body(sock, body, -1)

		if re.match('.*[Cc]ontent-[Ee]ncoding:[ \t]*gzip.*', self.headers, re.DOTALL):
			try:
				body = zlib.decompress(self.body, 16+zlib.MAX_WBITS).decode()
				self.body = body
			except Exception as e:
				log.Error(e)
		else:
			try:
				data = self.body.decode('utf8')
				self.body = data
			except Exception as e:
				log.Error(e)

	def http(self, url, headers):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.host, 80))
		sock.settimeout(self.SETTIMEOUT)
		sock.send(headers)
		self.recv(sock, url)

	def https(self, url, headers):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		context = ssl._create_default_https_context()
		context.check_hostname = self.host
		sock = context.wrap_socket(sock, server_hostname=self.host)
		try:
			sock.connect((self.host, 443))
		except Exception as e:
			log.Error(str(e))
			return None
		sock.settimeout(self.SETTIMEOUT)
		sock.write(headers)
		self.recv(sock, url)

	def download(self, path, method="get", headers={}, body=""):
		trun = time()
		self.setvar()
		method = method.upper()

		data = self.create_request(path, method, body, headers)
		if self.ssl:
			protocol = 'https'
			self.https(path, data)
		else:
			protocol = 'http'
			self.http(path, data)
		if self.body is not None:
			self.content_length = len(self.body)

		url = "{}://{}{}".format(protocol, self.host, path)
		log.Info("{} {} {} {} {}".format(method, url, self.status, self.content_length, time() - trun))
