from ..src.tools	import print_debug
from .dailymotion	import Dailymotion_Analyzer
from .peertube		import Peertube_Analyzer
from .youtube		import Youtube_Analyzer

def return_Analyzer(site):
	if site == '[youtube]':
		return Youtube_Analyzer
	elif site == '[dailymotion]':
		return Dailymotion_Analyzer
	elif site == '[peertube]':
		return Peertube_Analyzer
	else:
		print_debug('[!] Analyzer not found ({})'.format(site))
		return None
