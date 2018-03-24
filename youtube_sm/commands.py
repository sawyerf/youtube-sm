import time
import os
import sys
from .src.analyzer import (
	html_init,
	init,
	html_end,
	raw_end,
	list_end)
from .src.swy import (
	swy,
	generate_swy)
from .src.time import lcl_time

def check_id(id):
	if id[:2] == 'UC' or id[:2] == 'PL':
		return True
	else:
		return False

def main():
	url_data = []
	analyze = False
	analyze_only_one = False
	mode = 'html'
	count = 7
	sub_file = 'subscription_manager'
	#path
	if os.name == 'nt':
		path = os.path.expanduser('~') + '/.youtube_sm/'
	else:
		if os.uname().sysname == 'Linux':
			path = os.environ['HOME'] + '/.cache/youtube_sm/'
	try:
		os.makedirs(path + 'data/')
	except:
		pass
	#commands
	del sys.argv[0]
	if sys.argv==[]:
		passe = time.time()
		url_data = swy(path=path)
		html_init(path)
		nb_new = init(url_data, lcl_time(), path=path)
		html_end(path=path)
		open(path + 'log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("%H%M") + '\n')
	elif sys.argv == ['-h']:
		print("""Usage: youtube-sm [OPTIONS]

Options:
   -h                  Print this help text and exit
   -n  [file]          To use an other xml file for yours subscriptions
   -m  [mode]          The type of file do you want (html, raw, list)
   -t  [nb of days]    Numbers of days of subscriptions do you want in your file
   -d                  Show the dead channels + those who posted no videos
   -o  [nb of months]  Show the channels who didn't post videos in nb of months + dead channels
   -l  [id]            If you want to analyze only one channel or playlist
   -r                  To remove the cache before analyze
   -s  [id/all]        To have the stat of the channel(s)
   -a  [id]            To append a channel or a playlist at the end of sub.
   --init [file]       Remove all your subs and the cache and init with your subscription file.
   --af [file]         To append a file with list of channel or a playlist in sub.swy
   --ax [file]         To append a xml file in sub.swy
   --cat               To read 'sub.swy'
""", end='')
	else:
		for arg in range(len(sys.argv)):
			if sys.argv[arg][0] != '-':
				continue
			if sys.argv[arg][1] != '-':
				if sys.argv[arg] == '-o':
					from .src.channel_analyzer import old
					url_data = swy(path=path)
					print('[*]Start of analysis')
					try:
						min_tps = int(sys.argv[arg + 1])
					except:
						old(url_data)
					else:
						old(url_data, min_tps)
				elif sys.argv[arg] == '-d':
					from .src.channel_analyzer import dead
					url_data = swy(path=path)
					print('[*]Start of analysis')
					dead(url_data)
				elif sys.argv[arg] == '-m':
					analyze = True
					if sys.argv[arg + 1] in ['html', 'raw', 'list']:
						mode = sys.argv[arg + 1]
					else:
						exit('[!] Mode file invalid')
				elif sys.argv[arg] == '-t':
					analyze = True
					try:
						count = int(sys.argv[arg + 1])
					except:
						print('[!] Numbers of day invalid')
						exit()
				elif sys.argv[arg] == '-n':
					if os.path.exists(sys.argv[arg + 1]):
						if os.path.exists(path + 'sub.swy'):
							os.remove(path + 'sub.swy')
						generate_swy(sys.argv[arg + 1], path)
					else:
						exit('[!] File not found')
				elif sys.argv[arg] == '-a':
					if sys.argv[arg + 1][:2] in ['UC', 'PL']:
						add_sub([sys.argv[arg + 1]], path)
					else:
						print('[!] Id is not available')
				elif sys.argv[arg] == '-l':
					analyze = True
					analyze_only_one = True
					if sys.argv[arg + 1][:2] in ['UC', 'PL']:
						url_data = [sys.argv[arg + 1]]
					else:
						print('[!] Id is not available')
				elif sys.argv[arg] == '-r':
					from shutil import rmtree
					if os.path.exists(path + 'data'):
						rmtree(path + 'data')
					else:
						print('[!] Data do not exist')
				elif sys.argv[arg] == '-s':
					try:
						if check_id(sys.argv[arg+1]):
							from .src.channel_analyzer import stat
							stat(sys.argv[arg+1])
						elif sys.argv[arg+1] == 'all':
							from .src.channel_analyzer import stats
							subs = swy(path=path, liste=False)
							stats(subs)
						else:
							exit("[!] Id is not available")
					except IndexError:
						exit("[!] Missing argument after the '-s'")
			else:
				if sys.argv[arg] == '--af':
					if os.path.exists(sys.argv[arg + 1]):
						add_sub(open(sys.argv[arg + 1], 'r').read().split('\n'), path)
					else:
						exit('[!] File not found')
				elif sys.argv[arg] == '--ax':
					if os.path.exists(sys.argv[arg + 1]):
						generate_swy(sys.argv[arg + 1], path)
					else:
						exit('[!] File not found')
				elif sys.argv[arg] == '--cat':
					if os.path.exists(path + 'sub.swy'):
						with open(path + 'sub.swy', 'r') as file:
							while True:
								line = file.readline()
								if line == '':
									break
								try:
									print(line, end='')
								except:
									print(line.encode())
				elif sys.argv[arg] == '--init':
					from shutil import rmtree
					if os.path.exists(path):
						rmtree(path)
					try:
						os.makedirs(path + 'data/')
					except:
						exit('[*] Error We Can\'t Create The Folder')
					else:
						print('[*] Data File Create')
					if len(sys.argv) != arg + 1:
						add_file = sys.argv[arg + 1]
						if not os.path.exists(add_file):
							exit('[!] File Not Found (' + add_file + ')')
						if add_file[len(add_file) - 4] == '.swy':
							with open(add_file, 'r') as file:
								with open(path + 'sub.swy', 'a') as sub_file:
									nb_line = 1
									while True:
										line = file.readline()
										if '\t' in line:
											sub_file.write(line)
										else:
											if line == '':
												pass
											else:
												print('[!] No tabs in line ' + nb_line)
						else:
							url_data = swy(add_file, path=path)
					else:
						if os.path.exists('subscription_manager'):
							url_data = swy('subscription_manager', path=path)
						else:
							exit('[!] File Not Found (subscription_manager)')
					print('[*] Subs append to sub.swy')
					exit('[*] Done')
	if analyze:
		passe = time.time()
		if not analyze_only_one:
			url_data = swy(sub_file, path=path)
		if mode == 'html':
			html_init()
		elif mode == 'raw':
			if os.path.exists('sub_raw'):
				os.remove('sub_raw')
		elif mode == 'list':
			if os.path.exists('sub_list'):
				os.remove('sub_list')
		nb_new = init(url_data, lcl_time(), path, mode)
		if mode == 'html':
			html_end(count, path)
		elif mode ==  'raw':
			raw_end(count)
		elif mode == 'list':
			list_end(count)
		open(path + 'log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("    %H%M") + '\n')
