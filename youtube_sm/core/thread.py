from threading import Thread
from ..analyzer.imports import return_Analyzer
from datetime import (
	datetime,
	timedelta,
)
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
	for site in urls:
		analyzer = return_Analyzer(site)
		if analyzer is None:
			continue
		for i in range(len(urls[site])):
			thr = analyzer(urls[site][i])
			thr.initialize(method, file, prog)
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


def old(subs, days=365):
	since = datetime.now() - timedelta(days=days)
	threads = []
	for site in subs:
		Analyzer = return_Analyzer(site)
		if Analyzer is None:
			continue
		analyzer = Analyzer()
		for url in subs[site]:
			thr = Thread(target=analyzer.old, args=(url, since))
			threads.append(thr)
			thr.start()
	for i in threads:
		i.join()


def dead(subs):
	threads = []
	for site in subs:
		Analyzer = return_Analyzer(site)
		if Analyzer is None:
			continue
		analyzer = Analyzer()
		for url in subs[site]:
			thr = Thread(target=analyzer.dead, args=(url,))
			threads.append(thr)
			thr.start()
	for i in threads:
		i.join()
