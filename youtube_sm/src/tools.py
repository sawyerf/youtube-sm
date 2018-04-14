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

def type_id(id):
	"""True = Channel; False = Playlist"""
	if id[:2] == 'UC':
		return True
	elif id[:2] == 'PL':
		return False
	else:
		return True
