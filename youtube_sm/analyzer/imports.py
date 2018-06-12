from ..src.tools import print_debug
from .dailymotion import Dailymotion_Analyzer
from .youtube import Youtube_Analyzer

def return_Analyzer(site):
	if site == '[youtube]':
		return Youtube_Analyzer
	elif site == '[dailymotion]':
		return Dailymotion_Analyzer
	else:
		print_debug('[!] Analyzer not found ({})'.format(site))
		return None