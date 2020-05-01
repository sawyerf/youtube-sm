import re
from datetime  import datetime
from threading import Thread


class Analyzer(Thread):
	"""
	Common Function to all Analyzers
	"""
	NO_IMG='https://sawyerf.gitlab.io/youtube_sm/pixel.png'
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
				if 'date' in match:
					try:
						content[var] = datetime.strptime(content[var], match['date'])
					except:
						return None
		return content
