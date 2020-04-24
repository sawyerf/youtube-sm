import re
from threading			import Thread

class Analyzer(Thread):
	"""
	Common Function to all Analyzers
	"""
	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.real_analyzer()
		if self.prog != None:
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
