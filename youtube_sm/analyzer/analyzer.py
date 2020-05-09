import re
from datetime  import datetime
from threading import Thread
from ..core.tools import log


class Analyzer(Thread):
	"""
	Common Function to all Analyzers
	"""
	NO_IMG='https://sawyerf.gitlab.io/youtube_sm/pixel.png'
	def __sub_init__(self):
		self.method = '0'
		self.prog = None
		self.file = None

	def initialize(self, method='0', file=None, prog=None):
		self.method = method
		self.prog = prog
		self.file = file

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.real_analyzer()
		if self.prog is not None:
			self.prog.add()

	def match(self, url):
		return re.match(self.URL_MATCH, url)

	def extract_id(self, url):
		if url == '':
			return ''
		match = self.match(url)
		if not match:
			return url
		return match.group('ID')

	def info(self, item, matchs):
		content = {}
		for var, match in matchs.items():
			if 're' not in match:
				if 'default' in match:
					content[var] = match['default']
					continue
				else:
					return None
			find = re.findall(match['re'], item)
			i = 0
			if 'i' in match:
				i = match['i']
			if len(find) <= i:
				if 'default' not in match:
					return None
				content[var] = match['default']
			else:
				content[var] = find[i]
				if 'func' in match:
					content[var] = match['func'](content[var])
					if content[var] is None:
						return None
				elif 'date' in match:
					try:
						content[var] = datetime.strptime(content[var], match['date'])
					except:
						return None
		return content

	ISOK=0
	ISEMPTY=1
	ISDEAD=2
	def subis(self, text, status):
		if status == self.ISDEAD:
			log.Error('[CHANNEL DEAD] ', text)
		elif status == self.ISEMPTY:
			log.Error('[ NO CONTENT ] ', text)
		elif type(status) == datetime:
			log.RWarning('[ {} ] {}'.format(status.strftime('%Y-%m-%d'), text))
		elif status == self.ISOK:
			log.RInfo('[     OK     ] ', text)

	def old(self, sub, since):
		pass

	def dead(self, sub):
		pass
