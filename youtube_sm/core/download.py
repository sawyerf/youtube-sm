from time   import time
from .tools import log

import socket
import ssl
import re
import zlib


class Download():
	LANGUAGE = 'en'
	SETTIMEOUT = 0.1
	TIMEOUT = 10
	USERAGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'

	def __init__(self, https, host):
		self.ssl  = https
		self.host = host
		self.setvar()
		self.protocol = 'http'
		self.port = 80
		if self.ssl:
			self.protocol = 'https'
			self.port = 443

	def setvar(self):
		self.status  = ''
		self.headers = ''
		self.body    = ''

	def create_request(self, path, method, body, headers):
		req = "{} {} HTTP/1.1\r\n".format(method, path)

		default = {
			'Host': self.host,
			'User-Agent': self.USERAGENT,
			'Accept': '*/*',
			'Accept-Encoding': 'gzip',
			'Accept-Language': self.LANGUAGE
		}
		for key in headers:
			default[key] = headers[key]
		if body is not None:
			default["Content-Length"] = str(len(body))
		for name in default:
			req += '{}: {}\r\n'.format(name, default[name])
		req += "\r\n"
		if body is not None:
			req += body
		return req.encode()

	def real_recv(self):
		try:
			raw_data = self.sock.recv(100000)
			return raw_data
		except socket.timeout:
			return b''
		except Exception as e:
			log.Error('Error Recv: {}'.format(e))
			return b''

	def recv_headers(self):
		data = b''
		trun = time()
		while True:
			data += self.real_recv()
			if b'\r\n\r\n' in data:
				self.headers = data.split(b'\r\n\r\n')[0].decode() + '\r\n\r\n'
				len_headers = len(self.headers)
				self.status = re.findall(r'HTTP/1\.1 ([0-9]*)', self.headers)[0]
				data = data[len_headers:]
				if self.status != '100':
					return data
				trun = time()
			elif time() - trun > self.TIMEOUT:
				return None

	def recv_body(self, data, dlen):
		trun = time()
		while True:
			data += self.real_recv()
			if (dlen == -1 and time() - trun > self.TIMEOUT) \
				or (dlen != -1 and dlen <= len(data)):
				return data

	def recv_chunk_body(self, chunk):
		dlen = 0
		data = b''
		chunk = b'\r\n' + chunk
		while True:
			while dlen + 2 < len(chunk) and b'\r\n' in chunk[dlen + 2:]:
				data += chunk[:dlen]
				chunk = chunk[dlen + 2:]
				str_dlen = chunk.split(b'\r\n')[0].decode()
				dlen = int(str_dlen, 16)
				if dlen == 0:
					return data
				chunk = chunk[len(str_dlen) + 2:]
			chunk += self.real_recv()

	def recv(self):
		body = self.recv_headers()
		if self.headers == '' or self.status == '204' or body is None:
			return
		if re.match('.*[Cc]ontent-[Ll]ength:', self.headers, re.DOTALL):
			dlen = int(re.findall('[Cc]ontent-[Ll]ength: ([0-9]*)', self.headers)[0])
			body = self.recv_body(body, dlen)
		elif re.match('.*[Tt]ransfer-[Ee]ncoding:[ \t]*[Cc]hunked', self.headers, re.DOTALL):
			body = self.recv_chunk_body(body)
		else:
			body = self.recv_body(body, -1)

		try:
			if re.match('.*[Cc]ontent-[Ee]ncoding:[ \t]*gzip', self.headers, re.DOTALL):
				self.body = zlib.decompress(body, 16+zlib.MAX_WBITS).decode()
			else:
				self.body = body.decode('utf8')
		except Exception as e:
			log.Error(e)

	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.ssl:
			context = ssl._create_default_https_context()
			context.check_hostname = self.host
			self.sock = context.wrap_socket(self.sock, server_hostname=self.host)
		self.sock.settimeout(3)
		self.sock.connect((self.host, self.port))

	def download(self, path, method="get", headers={}, body=None, status='200'):
		trun = time()
		self.setvar()
		method = method.upper()

		request = self.create_request(path, method, body, headers)
		try:
			self.connect()
		except Exception as e:
			log.Error(str(e))
			return
		self.sock.send(request)
		self.sock.settimeout(self.SETTIMEOUT)
		self.recv()

		url = "{}://{}{}".format(self.protocol, self.host, path)
		if self.status == status:
			log.Info("{} {} {} {} {}".format(method, url, self.status, len(self.body), time() - trun))
		else:
			log.Warning("{} {} {} {} {}".format(method, url, self.status, len(self.body), time() - trun))
