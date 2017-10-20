from urllib.request import *
from youtube.analyzer import *
from youtube.swy import *
from youtube.time import *
import time
import os
import sys

def swy(sub_file='subscription_manager'):
	url_data = []
	if not os.path.exists('sub.swy'):
		generate_swy(sub_file)
	data_sub = open('sub.swy', 'r').read().split('\n')
	for i in data_sub:
		url_data.append(i.split('\t')[0])
	return url_data


url_data = []
analyze = False
mode = 'html'
count = 7
sub_file = 'subscription_manager'
#commands
del sys.argv[0]
if sys.argv==[]:
	passe = time.time()
	url_data = swy()
	html_init()
	nb_new = analyzer_sub(url_data, lcl_time())
	html_end()
	open('log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("%H%M") + '\n')
elif sys.argv == ['-h']:
	print("""
Usage: python3 youTube.py [OPTIONS]

Options:
	-h			Print this help text and exit
	-m [mode] 		The type of file do you want (html, raw)
	-t [nb of days]		Numbers of days of subscriptions do you want in your file
	-d			Show the dead channels + those who posted no videos
	-o [nb of months]	Show the channels who didn't post videos in nb of months + dead channels
""", end='')
else:
	for arg in range(len(sys.argv)):
		if sys.argv[arg] == '-o':
			from youtube.channel_analyzer import *
			url_data = swy()
			print('[*]Start of analysis')
			try:
				min_tps = int(sys.argv[arg + 1])
			except:
				old(url_data)
			else:
				old(url_data, min_tps)
		elif sys.argv[arg] == '-d':
			from youtube.channel_analyzer import *
			url_data = swy()
			print('[*]Start of analysis')
			dead(url_data)
		elif sys.argv[arg] == '-m':
			analyze = True
			if sys.argv[arg + 1] in ['html', 'raw']:
				mode = sys.argv[arg + 1]
			else:
				print('[!] Mode file invalid')
				exit()
		elif sys.argv[arg] == '-t':
			analyze = True
			try:
				count = int(sys.argv[arg + 1])
			except:
				print('[!] Numbers of day invalid')
				exit()
		elif sys.argv[arg] == '-n':
			analyze = True
			if os.path.exists(sys.argv[arg + 1]):
				sub_file = sys.argv[arg + 1]
			else:
				print('[!] File not found')
if analyze:
	passe = time.time()
	url_data = swy(sub_file)
	if mode == 'raw':
		if os.path.exists('sub_raw'):
			os.remove('sub_raw')
	html_init()
	nb_new = analyzer_sub(url_data, lcl_time(), mode)	
	if mode == 'html':
		html_end(count)
	elif mode ==  'raw':
		raw_end()
