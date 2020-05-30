from ..analyzer.imports import *
from .thread import *
from .write import Write_file
from .swy import *

def TestAnalyzer(path):
	since = -1
	for method in ['0', '1']:
		log.Info('Method: ', method)
		for anal in analyzers:
			url_tests = anal.TEST
			for sub in url_tests:
				file = Write_file(None, None, 'html', method, since)
				url = {anal.SITE: [sub]}
				log.RInfo('Start sub="', sub, '", method=', method)
				Run_analyze(url, False, file, method)
				if len(file.contents) == 0:
					log.RWarning('{}: No content found'.format(sub))
				else:
					log.RInfo('{}: {} contents has been found'.format(sub, len(file.contents)))
				for mode in ['html', 'json', 'list', 'raw']:
					file.mode = mode
					file.write()
	log.RInfo('Start Old and Dead')
	for anal in analyzers:
		for since in [1, 365]:
			url_tests = anal.TEST
			for sub in url_tests:
				url = {anal.SITE: [sub]}
				old(url, since)
				dead(url)
	log.RInfo('Start Add Sub')
	for anal in analyzers:
		url = {anal.SITE: anal.TEST}
		add_sub(url, '')
