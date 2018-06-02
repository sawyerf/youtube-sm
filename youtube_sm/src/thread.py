from threading import Thread
from ..analyzer.imports import return_Analyzer
from ..src.tools import (
	Progress,
	Progress_loop,
	type_id)

def Run_analyze(urls, output, min_date, path='', mode='html', loading=False, file=None, method='0'):
	"""Run all the analyze in a thread"""
	threads = []
	ending = 0
	nb = len(urls)
	if loading and nb == 1:
		prog = Progress_loop()
		prog.progress_bar()
	elif loading and nb > 1:
		prog = Progress(nb)
		prog.progress_bar()
	else:
		prog = None
	if method == '0':
		max_thr = 200
	elif method == '1':
		max_thr = 50
	elif method == '2':
		max_thr = 5
	# Run threads
	for site in urls:
		analyzer = return_Analyzer(site)
		if analyzer == None:
			continue
		for i in range(len(urls[site])):
			thr = analyzer(urls[site][i], min_date, mode, method, file, prog)
			thr.Thread()
			threads.append(thr)
			thr.start()
			if i%max_thr == 0 or nb == i+1:
				for y in threads:
					y.join()
				threads = []
	if loading and prog.xmin != prog.xmax:
		prog.xmin = prog.xmax
		prog.progress_bar()
		print()
