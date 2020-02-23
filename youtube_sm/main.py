import time
import os
import sys

from .src.commands import Commands
from .src.tools import (
	log)

def getpath():
	if os.name == 'nt':
		path = os.path.expanduser('~') + '/.youtube_sm/'
	else:
		if os.uname().sysname == 'Linux' or os.uname().sysname == 'Darwin':
			path = os.environ['HOME'] + '/.cache/youtube_sm/'
	return path

def main():
	# Init variable
	# Path of the cache
	log.info('Hello :)')
	try:
		path = getpath()
	except KeyError:
		log.error('HOME is not set')
		exit()
	log.info('Path: {}'.format(path))
	try:
		os.makedirs(path + 'data/')
	except:
		log.warning('Data already exist or can\'t be create')
	del sys.argv[0]
	cmd = Commands(path)
	cmd.parser()
	cmd.router()
