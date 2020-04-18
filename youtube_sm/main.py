import time
import os
import sys

from .core.commands import Commands
from .core.tools import (
	log)
from .version	import __version__

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
	try:
		path = getpath()
	except KeyError:
		log.Error('HOME is not set')
		exit()
	log.cache = path + 'verbose.log'
	log.Info('Hello :)')
	log.Info('Version: ', __version__)
	log.Info('Path: {}'.format(path))
	try:
		os.makedirs(path + 'data/')
	except:
		log.Warning('Data already exist or can\'t be create')
	del sys.argv[0]
	cmd = Commands(path)
	cmd.parser()
	cmd.router()
