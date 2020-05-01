import os
import sys

from .core.commands import Commands
from .core.tools import (
	log
)
from .version import __version__
from datetime import datetime


def getpath():
	if os.name == 'nt':
		path = os.path.expanduser('~') + '/.youtube_sm/'
	else:
		if os.uname().sysname == 'Linux' or os.uname().sysname == 'Darwin':
			try:
				path = os.environ['HOME'] + '/.cache/youtube_sm/'
			except KeyError:
				log.Error('HOME is not set')
				exit()
	return path

def createcache():
	path = getpath()
	if not os.path.exists(path + 'data/'):
		try:
			os.makedirs(path + 'data/')
		except:
			log.Warning('Data can\'t be create')
			exit()
	log.cache = path + 'verbose.log'
	return path

def main():
	path = createcache()
	log.Info('Hello :)')
	log.Info('Date: ', datetime.now())
	log.Info('Version: ', __version__)
	log.Info('Path: ', path)
	del sys.argv[0]
	cmd = Commands(path)
	cmd.parser()
	cmd.router()
