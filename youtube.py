from urllib.request import *
from youtube_html import *
import time
import os

tps = time.localtime()
tm_year, tm_mon, tm_mday = tps.tm_year, tps.tm_mon, tps.tm_mday
url_data = []

html_init()
if len(str(tm_mon)) == 1:
	if tm_mon==1:
		tm_year = str(tm_year - 1)
		tm_mon = '12'
	else:
		tm_year = str(tm_year)
		tm_mon = '0' + str(tm_mon - 1)
elif len(str(tm_mday)) == 1:
	tm_mday = '0' + str(tm_mday)
else:
	if tm_mon == 1:
		tm_year = str(tm_year - 1)
		tm_mon = '12'
	else:
		tm_mon = str(tm_mon - 1)
tm_mday = str(tm_mday)
lcl_tps = int(tm_year + tm_mon + tm_mday + '000000')


data_sub = open('subscription_manager', 'r').read().split('xmlUrl="')
del data_sub[0]
for i in data_sub:
	url_data.append(i.split('"')[0])

passe = time.time()
for url in url_data:
	nb = 0
	while nb!=5:
		try:
			data = urlopen(url).read().decode()
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

print(time.time() - passe)
fch = sorted(os.listdir('data/'))
for i in range(7):
	fch_in = sorted(os.listdir('data/' + fch[-1-i]))
	for a in range(len(fch_in)):
		data = open('data/' + fch[-1-i] + '/' + fch_in[-1-a], 'r').read()
		open('sub.html', 'a').write(data)
