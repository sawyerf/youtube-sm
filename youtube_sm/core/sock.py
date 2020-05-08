import socket
import ssl
import re
import zlib

from .download import Download
from .tools import log

TIMEOUT = 2

def download_http(host, url, useragent=Download.USERAGENT):
	site = Download(False, host)
	site.USERAGENT = useragent
	site.download(url)
	return site

def download_https(host, url, useragent=Download.USERAGENT):
	site = Download(True, host)
	site.USERAGENT = useragent
	site.download(url)
	return site
