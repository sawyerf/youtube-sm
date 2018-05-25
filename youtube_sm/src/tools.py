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
		for i in range(int(40 - pc*40 + (pc*40)%1)):
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

def type_id(id):
	"""True = Channel; False = Playlist"""
	if id[:2] == 'UC':
		return True
	elif id[:2] == 'PL':
		return False
	else:
		return True

def check_id(id):
	if id[:2] == 'UC' or id[:2] == 'PL':
		return True
	else:
		return False

def del_data(path='', prin=True):
	""" delete the data folder"""
	from shutil import rmtree
	import os
	if os.path.exists(path + 'data'):
		for i in range(2):
			try:
				rmtree(path + 'data')
			except:
				pass
			else:
				continue
		try:
			os.makedirs(path + 'data/')
		except:
			pass
	else:
		if prin:
			print('[!] Data do not exist')
