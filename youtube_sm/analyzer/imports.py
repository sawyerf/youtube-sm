from ..core.tools	import log
from .dailymotion	import Dailymotion_Analyzer
from .infoconcert	import InfoConcert_Analyzer
from .peertube		import Peertube_Analyzer
from .youtube		import Youtube_Analyzer

analyzers = [
	Dailymotion_Analyzer,
	InfoConcert_Analyzer,
	Peertube_Analyzer,
	Youtube_Analyzer,
]

def return_Analyzer(site):
	for anal in analyzers:
		if anal.SITE == site:
			return anal
	log.Error('Analyzer not found ({})'.format(site))
	return None

def UrlToAnalyzer(url):
	for anal in analyzers:
		if anal().match(url):
			return anal
	return None
