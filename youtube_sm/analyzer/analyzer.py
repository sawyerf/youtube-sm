import re

class Analyzer():
	def match(self, url):
		return re.match(self.URL_MATCH, url)

	def extract_id(self, url):
		if url == '':
			return ''
		match = self.match(url)
		if not match:
			return url
		return match.group('ID')
