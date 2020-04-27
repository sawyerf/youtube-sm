import socket
import ssl
import re
import zlib

from .download import Download
from .tools import log

TIMEOUT = 2

def download_http(url, host='www.youtube.com'):
	site = Download(False, host)
	site.download(url)
	return site

def download_https(url, host='www.youtube.com'):
	site = Download(True, host)
	site.download(url)
	return site
