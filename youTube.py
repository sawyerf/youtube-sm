from urllib.request import *
from youtube.html import *
from youtube.swy import *
from youtube.time import *
import time
import os

url_data = []
nb_new = 0

html_init()
min_date = lcl_time()

try:
	data_sub = open('sub.swy', 'r').read().split('\n')
except:
	generate_swy()
	data_sub = open('sub.swy', 'r').read().split('\n')

for i in data_sub:
	url_data.append(i.split('\t')[0])

passe = time.time()
nb_news = html_start(url_data, min_date)

open('log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("%H%M") + '\n')

html_end()
