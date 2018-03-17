from src.analyzer import *
from src.swy import *
from src.time import *
import time
import os
import sys

def swy(sub_file='subscription_manager', liste=True):
	if not os.path.exists('sub.swy'):
		generate_swy(sub_file)
	data_sub = open('sub.swy', 'rb').read().decode("utf8").split('\n')
	if liste:
		url_data = []
		for i in data_sub:
			url_data.append(i.split('\t')[0])
	else:
		url_data = dict()
		for i in data_sub:
			ch = i.split('\t')
			try:
				url_data[ch[0]] = ch[1]	
			except:
				pass
	return url_data

def check_id(id):
	print(id[:2])
	if id[:2] == 'UC' or id[:2] == 'PL':
		return True
	else:
		return False
	

url_data = []
analyze = False
analyze_only_one = False
mode = 'html'
count = 7
sub_file = 'subscription_manager'
#commands
del sys.argv[0]
if sys.argv==[]:
	passe = time.time()
	url_data = swy()
	html_init()
	nb_new = init(url_data, lcl_time())
	html_end()
	open('log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("%H%M") + '\n')
elif sys.argv == ['-h']:
	print("""
Usage: python3 youTube.py [OPTIONS]

Options:
	-h			Print this help text and exit
	-n  [file]		To use an other xml file for yours subscriptions
	-m  [mode] 		The type of file do you want (html, raw, list)
	-t  [nb of days]	Numbers of days of subscriptions do you want in your file
	-d			Show the dead channels + those who posted no videos
	-o  [nb of months]	Show the channels who didn't post videos in nb of months + dead channels
	-a  [id]		To append a channel or a playlist at the end of sub.swy
	-af [file]		To append a file with list of channel or a playlist in sub.swy
	-ax [file]		To append a xml file in sub.swy
	-l  [id]		If you want to analyze only one channel or playlist
	-r			To remove the cache before analyze
	-s  [id/all]		To have the stat of the channel(s)
""", end='')
else:
	for arg in range(len(sys.argv)):
		if sys.argv[arg] == '-o':
			from src.channel_analyzer import *
			url_data = swy()
			print('[*]Start of analysis')
			try:
				min_tps = int(sys.argv[arg + 1])
			except:
				old(url_data)
			else:
				old(url_data, min_tps)
		elif sys.argv[arg] == '-d':
			from src.channel_analyzer import *
			url_data = swy()
			print('[*]Start of analysis')
			dead(url_data)
		elif sys.argv[arg] == '-m':
			analyze = True	
			if sys.argv[arg + 1] in ['html', 'raw', 'list']:
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
			if os.path.exists(sys.argv[arg + 1]):
				if os.path.exists('sub.swy'):
					os.remove('sub.swy')
				generate_swy(sys.argv[arg + 1])
			else:
				print('[!] File not found')
				exit()
		elif sys.argv[arg] == '-a':
			if sys.argv[arg + 1][:2] in ['UC', 'PL']:
				from src.swy import add_sub
				add_sub([sys.argv[arg + 1]])
			else:
				print('[!] Id is not available')
		elif sys.argv[arg] == '-af':
			if os.path.exists(sys.argv[arg + 1]):
				from src.swy import add_sub
				add_sub(open(sys.argv[arg + 1], 'r').read().list('\n'))
			else:
				print('[!] File not found')
				exit()
		elif sys.argv[arg] == '-ax':
			if os.path.exists(sys.argv[arg + 1]):
				generate_swy(sys.argv[arg + 1])
			else:
				print('[!] File not found')
				exit()
		elif sys.argv[arg] == '-l':
			analyze = True
			analyze_only_one = True
			if sys.argv[arg + 1][:2] in ['UC', 'PL']:
				url_data = [sys.argv[arg + 1]]
			else:
				print('[!] Id is not available')
		elif sys.argv[arg] == '-r':
			from shutil import rmtree
			if os.path.exists('data'):
				rmtree('data')
			else:
				print('[!] Data do not exist')
		elif sys.argv[arg] == '-s':
			if check_id(sys.argv[arg+1]):
				from src.channel_analyzer import stat
				stat(sys.argv[arg+1])
			elif sys.argv[arg+1] == 'all':
				from src.channel_analyzer import stats
				subs = swy(liste=False)
				stats(subs)
			else:
				print("[!] Id is not available")

if analyze:
	passe = time.time()
	if not analyze_only_one:
		url_data = swy(sub_file)
	if mode == 'html':
		html_init()
	elif mode == 'raw':
		if os.path.exists('sub_raw'):
			os.remove('sub_raw')
	elif mode == 'list':
		if os.path.exists('sub_list'):
			os.remove('sub_list')
	nb_new = init(url_data, lcl_time(), mode)	
	if mode == 'html':
		html_end(count)
	elif mode ==  'raw':
		raw_end(count)
	elif mode == 'list':
		list_end(count)
	open('log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("    %H%M") + '\n')	
