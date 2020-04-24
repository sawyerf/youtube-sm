from threading import Thread
from ..analyzer.imports import return_Analyzer
from .time import lcl_time
from .tools import (
	Progress,
	Progress_loop,
	log)


def Run_analyze(urls, loading=False, file=None, method='0'):
	"""Run all the analyze in a thread"""
	threads = []
	nb = 0
	for site in urls:
		nb += len(urls[site])
	if loading and nb == 1:
		prog = Progress_loop()
		prog.progress_bar()
	elif loading and nb > 1:
		prog = Progress(nb)
		prog.progress_bar()
	else:
		prog = None
	if method == '0':
		max_thr = 40
	elif method == '1':
		max_thr = 50
	elif method == '2':
		max_thr = 5
	# Run threads
	log.Info('Start threads')
	for site in urls:
		analyzer = return_Analyzer(site)
		if analyzer is None:
			continue
		for i in range(len(urls[site])):
			thr = analyzer(urls[site][i], method, file, prog)
			thr.Thread()
			threads.append(thr)
			log.Info("Thread start ({}{})".format(site, urls[site][i]))
			thr.start()
			if i > 1 and (i % max_thr == 0 or nb == i+1):
				for y in threads:
					y.join()
				threads = []
		for y in threads:
			y.join()
	if loading and prog.xmin != prog.xmax:
		prog.xmin = prog.xmax
		prog.progress_bar()
		print()


def old(subs, min_tps=12):
	lcl = lcl_time(min_tps * 31)
	threads = []
	log.Info('Start threads')
	for site in subs:
		analyzer = return_Analyzer(site)()
		for url in subs[site]:
			thr = Thread(target=analyzer.old, args=(url, lcl))
			threads.append(thr)
			thr.start()
	for i in threads:
		i.join()


def dead(subs):
	threads = []
	log.Info('Start threads')
	for site in subs:
		analyzer = return_Analyzer(site)()
		for url in subs[site]:
			thr = Thread(target=analyzer.dead, args=(url,))
			threads.append(thr)
			thr.start()
	for i in threads:
		i.join()
