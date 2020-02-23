from ..src.tools	import log
from .dailymotion	import Dailymotion_Analyzer
from .infoconcert	import InfoConcert_Analyzer
from .peertube		import Peertube_Analyzer
from .youtube		import Youtube_Analyzer

def return_Analyzer(site):
	if site == '[youtube]':
		return Youtube_Analyzer
	elif site == '[dailymotion]':
		return Dailymotion_Analyzer
	elif site == '[peertube]':
		return Peertube_Analyzer
	elif site == '[infoconcert]':
		return InfoConcert_Analyzer
	else:
		log.error('Analyzer not found ({})'.format(site))
		return None
