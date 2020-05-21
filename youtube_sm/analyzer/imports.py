from ..core.tools import log
from .infoconcert import InfoConcert_Analyzer
from .laquadrature import LaQuadrature_Analyzer
from .peertube    import Peertube_Analyzer
from .reddit      import Reddit_Analyzer
from .revolutionpermanente import RevolutionPermanente_Analyzer
from .youtube     import Youtube_Analyzer
from .twitter     import Twitter_Analyzer

analyzers = [
	InfoConcert_Analyzer,
	Peertube_Analyzer,
	Reddit_Analyzer,
	RevolutionPermanente_Analyzer,
	Youtube_Analyzer,
	LaQuadrature_Analyzer,
	Twitter_Analyzer,
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
