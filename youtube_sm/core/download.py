from time   import *
from .tools import log

import socket
import ssl
import re
import zlib


USERAGENT="Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0"
VHTTP="1.1"
LANG='en'

class Download():
	def __init__(self, https, host, inter=0.1, timeout=3):
		self.ssl  = https
		self.host = host
		self.lang = LANG
		self.useragent = USERAGENT
		self.vhttp = VHTTP
		self.inter = inter
		self.timeout = timeout
		self.response = ""
		self.body = ""
		self.headers = ""
		self.status = ""

	def create_req(self, url, method, body, headers, useragent):
		req = "{} {} HTTP/{}\n".format(method.upper(), url, self.vhttp)
		req += "Host: {}\n".format(self.host)

		headers['User-Agent'] = useragent
		if not 'Accept' in headers:
			headers['Accept'] = '*/*'
		if not 'Accept-Encoding' in headers:
			headers['Accept-Encoding'] = 'gzip'
		if not 'Accept-Language' in headers:
			headers['Accept-Language'] = self.lang
		if body is not None:
			headers["Content-Length"] = str(len(body))
		for name in headers:
			req += '{}: {}\n'.format(name, headers[name])
		req += "\n"
		req = req.replace("\n", "\r\n")
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
		self.headers = ''
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
				data = data[len_headers:]
			if time() - trun > self.timeout:
				self.headers = data.decode()
				return data

	def recv_body(self, sock, data, dlen):
		trun = time()
		while True:
			data += self.real_recv(sock)
			if ( dlen == -1 and time() - trun > self.timeout ) \
				or ( dlen != -1 and dlen <= len(data) ):
				self.body = data
				return data

	def recv_chunked_body(self, sock, data):
		trun = time()
		dlen = 0
		if b'\r\n' in data:
			dlen = data.split(b'\r\n')[0]
			len_dlen = len(dlen) + 2
			data = data[len_dlen:]
			dlen = int(dlen, 16)
			if dlen == 0:
				self.body = data
				return data
		if data == b'':
			data = b'\r\n'
		while True:
			data += self.real_recv(sock)
			while dlen < len(data) and b'\r\n' in data[dlen + 2:]:
				suite = data[dlen + 2:]
				if suite == b'':
					continue
				str_dlen = suite.split(b'\r\n')[0]
				try:
					if int(str_dlen, 16) == 0:
						data = data[:dlen]
						self.body = data
						return data
				except Exception as e:
					log.Error(e)
					return self.recv_body(sock, data, -1)
				len_dlen = len(str_dlen) + 2
				data = data[:dlen] + suite[len_dlen:]
				dlen += int(str_dlen, 16)

	def recv(self, sock, url):
		data = self.recv_headers(sock)
		if self.headers == '':
			return ''
		if self.status == '204':
			return self.headers + '\r\n\r\n'
		dlen = -1
		if re.match('.*[Cc]ontent-[Ll]ength: .*', self.headers, re.DOTALL):
			dlen = int(re.findall('[Cc]ontent-[Ll]ength: (.*)\r', self.headers)[0])
		else:
			sock.settimeout(1)
		if re.match('.*[Tt]ransfer-[Ee]ncoding:[ \t]*[Cc]hunked.*', self.headers, re.DOTALL):
			self.recv_chunked_body(sock, data)
		else:
			self.recv_body(sock, data, dlen)

		if re.match('.*[Cc]ontent-[Ee]ncoding:[ \t]*gzip.*', self.headers, re.DOTALL):
			try:
				body = zlib.decompress(self.body, 16+zlib.MAX_WBITS).decode()
				self.body = body
				return self.headers + '\r\n\r\n' + self.body
			except Exception as e:
				log.Warning('Can\'t decode data recv')
				log.Error(e)
		else:
			try:
				data = self.body.decode('utf8')
				self.body = data
				return self.headers + '\r\n\r\n' + self.body
			except Exception as e:
				log.Warning('Can\'t decode data recv')
				log.Error(e)
		return self.headers + '\r\n\r\n' + str(self.body)

	def http(self, url, headers):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.host, 80))
		sock.settimeout(self.inter);
		sock.send(headers)
		return self.recv(sock, url)

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
		sock.settimeout(self.inter)
		sock.write(headers)
		return self.recv(sock, url)

	def download(self, path, method="get", headers={}, body=""):
		trun = time()
		self.status   = ""
		self.response = ""
		self.headers  = ""
		self.body     = ""
		self.content_length = 0
		method        = method.upper()

		protocol = 'http'
		if self.ssl:
			protocol = 'https'
		self.url = "{}://{}{}".format(protocol, self.host, path)
		data = self.create_req(path, method, body, headers, self.useragent)
		if self.ssl:
			self.response = self.https(path, data)
		else:
			self.response = self.http(path, data)
		if not self.response in ["", None]:
			self.content_length = len(self.body)
		log.Info("{} {} {} {} {}".format(method, self.url, self.status, self.content_length, time() - trun))
		return self.response
