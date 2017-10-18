from urllib.request import *
from youtube.html import *
from youtube.swy import *
from youtube.time import *
import time
import os
import sys

url_data = []
nb_new = 0

if not os.path.exists('sub.swy'):
	generate_swy()
data_sub = open('sub.swy', 'r').read().split('\n')
for i in data_sub:
	url_data.append(i.split('\t')[0])

if sys.argv==None:
	html_init()
	min_date = lcl_time()
	passe = time.time()
	nb_news = html_start(url_data, min_date)
	html_end()
	open('log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("%H%M") + '\n')
else:
	for arg in range(len(sys.argv)):
		if sys.argv[arg] == '-o':
			from youtube.channel_analyzer import *
			print('[*]Start of analysis')
			try:
				min_tps = int(sys.argv[arg + 1])
			except:
				old(url_data)
			else:
				del sys.argv[arg + 1]
				old(url_data, min_tps)
			exit()
		elif sys.argv[arg] == '-d':
			from youtube.channel_analyzer import *
			print('[*]Start of analysis')
			dead(url_data)
		




