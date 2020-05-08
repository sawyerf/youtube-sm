import os
import sys
from shutil import rmtree
from time import time, strftime, gmtime

TRUN=time()


class Progress():
	"""Print a progress bar"""
	def __init__(self, xmax=0):
		self.xmin = 0
		self.xmax = xmax

	def add(self):
		self.xmin += 1
		self.progress_bar()

	def progress_bar(self):
		load = ''
		if self.xmax == 0:
			pc = 0
		else:
			pc = (self.xmin/self.xmax)
		for i in range(int(pc*40)):
			load += '█'
		for i in range(int(40 - pc * 40 + (pc * 40) % 1)):
			load += ' '
		print('{} %|{}| {}/{} analyzed'.format(str(pc*100)[:3], load, str(self.xmin), str(self.xmax)), end='\r')
		if pc == 1:
			print()


class Progress_loop():
	def __init__(self):
		self.x = 0
		self.bar = '          '
		self.xmin = None
		self.xmax = None

	def add(self):
		self.x += 1
		self.progress_bar()

	def progress_bar(self):
		self.x = self.x % 10
		print('|{}{}{}|'.format(self.bar[:self.x], '█', self.bar[self.x + 1:]), end='\r')


def del_data(path):
	"""
	delete the data folder
	"""
	if path is None:
		return
	if os.path.exists(path + 'data'):
		try:
			rmtree(path + 'data')
		except:
			pass
		os.makedirs(path + 'data/')
	else:
		log.Warning('Data folder don\'t exist')


def exit_debug(msg, i=0):
	if i == 0:
		log.RInfo(msg)
	elif i == 1:
		log.Error(msg)
	exit()


class log:
	cache=''

	def Info(*msg, end='\n'):
		log.print('\33[1;36m', '[*] ', msg, end, True)

	def Warning(*msg, end='\n'):
		log.print('\33[1;33m', '[!] ', msg, end, True)

	def RInfo(*msg, end='\n'):
		log.print('\33[1;36m', '[*] ', msg, end, False)

	def RWarning(*msg, end='\n'):
		log.print('\33[1;33m', '[!] ', msg, end, False)

	def Error(*msg, end='\n'):
		log.print('\33[1;31m', '[!] ', msg, end, False)

	def Join(msgs):
		fin = ''
		for msg in msgs:
			fin += str(msg)
		return fin

	def print(color, init, msgs, end, verbose_only):
		date = '[{}]'.format(strftime("%H:%M:%S", gmtime(time() - TRUN)))
		msg = log.Join(msgs)
		if (verbose_only and '-v' in sys.argv) or not verbose_only:
			print(color, init, msg, "\033[00m", end=end, sep='')
		if log.cache != '':
			open(log.cache, 'a').write(date + init + str(msg) + '\n')
