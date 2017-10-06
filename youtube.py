from urllib.request import *
from youtube_html import *
from process_swy import *
import time
import os

tps = time.localtime()
tm_year, tm_mon, tm_mday = tps.tm_year, tps.tm_mon, tps.tm_mday
url_data = []

html_init()
if tm_mon == 1:
	tm_mon = 12
	tm_year -= 1
else:
	tm_mon -= 1
tm_mday = str(tm_mday)
tm_mon = str(tm_mon)
tm_year = str(tm_year)
if len(tm_mday) == 1:
	tm_mday = '0' + tm_mday
elif len(tm_mon) == 1:
	tm_mon = '0' + tm_mon

lcl_tps = int(tm_year + tm_mon + tm_mday + '000000')

try:
	data_sub = open('sub.swy', 'r').read().split('\n')
except:
	generate_swy()
	data_sub = open('sub.swy', 'r').read().split('\n')

for i in data_sub:
	url_data.append(i.split('\t')[0])

passe = time.time()
for url in url_data:
	nb = 0
	while nb!=5:
		try:
			data = urlopen('https://www.youtube.com/feeds/videos.xml?channel_id=' +  url).read().decode()
		except:
			nb += 1
		else:
			break
	linfo = data.split("<entry>")
	del linfo[0]
	for i in linfo:
		date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
		if lcl_tps <= date:
			html_process(i)

open('log', 'a').write(str(time.time() - passe) + '\n')

fch = sorted(os.listdir('data/'))
for i in range(7):
	fch_in = sorted(os.listdir('data/' + fch[-1-i]))
	for a in range(len(fch_in)):
		data = open('data/' + fch[-1-i] + '/' + fch_in[-1-a], 'r').read()
		open('sub.html', 'a').write(data)
