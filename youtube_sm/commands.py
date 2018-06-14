import time
import os
import sys

from .src.write import (
	Write_file,
	write_css,
	write_log)
from .src.thread import Run_analyze
from .src.swy import (
	swy,
	generate_swy,
	add_sub,
	init_swy)
from .src.tools import (
	del_data,
	check_id,
	print_debug)
from .src.time import lcl_time


def main():
	# Init variable
	url_data = []
	analyze = False
	analyze_only_one = False
	loading = False
	method = '0'
	mode = 'html'
	count = 7
	all_time = False
	output = ''
	sub_file = 'subscription_manager'
	site = 'youtube'
	# Path of the cache
	print_debug('[*] Hello :)')
	if os.name == 'nt':
		path = os.path.expanduser('~') + '/.youtube_sm/'
	else:
		if os.uname().sysname == 'Linux' or os.uname().sysname == 'Darwin':
			path = os.environ['HOME'] + '/.cache/youtube_sm/'
	print_debug('[*] Path: {}'.format(path))
	try:
		os.makedirs(path + 'data/')
	except:
		print_debug('[!] Data already exist or can\'t be create')
	# Commands
	del sys.argv[0]
	if sys.argv==[]: # Default command
		passe = time.time()
		url_data = swy(path)
		file = Write_file('sub.html', path, 'html', '0')
		file.html_init()
		Run_analyze(url_data, 'sub.html', lcl_time(), path, 'html', False, file, '0')
		file.html_json_end()
		write_log(sys.argv, path, passe)
	elif sys.argv == ['-h'] or sys.argv == ['--help']:
		print("""Usage: youtube-sm [OPTIONS]

Options:
   -h                     Print this help text and exit
   -m     [mode]          Choose the type of the output (html, json, raw, list, view)
   -t     [nb of days]    Choose how far in the past do you want the program to look for videos
   -d                     Show the dead channels + those who posted no videos
   -o     [nb of months]  Show the channels who didn't post videos in [nb of months] + dead channels
   -l     [site][id]      Analyze only one channel or playlist
   -r                     Remove the cache
   -s     [id/all]        Outputs the stats of the selected channel(s)
   -a     [site][id]      Append a channel or a playlist at the end of sub.
   --init [file]          Remove all your subs and the cache and init with your subscription file.
   --af   [file]          Append a file with list of channel or a playlist in sub.swy
   --ax   [file]          Append a xml file in sub.swy
   --html                 Recover yours subs in the common page web (more videos)
   --ultra-html           Recover all the videos with the common page and the button 'load more'
   --output [file]        Choose the name of the output file
   --cat                  View your subscriptions
   --css  [style]         Import the css files (light, dark, switch)
   --debug                Print errors and progress
   --loading              Prints a progress bar while running
""", end='')
	else:
		for arg in range(len(sys.argv)):
			if sys.argv[arg][0] != '-':
				continue
			if sys.argv[arg][1] != '-':
				if sys.argv[arg] == '-o':
					from .src.thread import old
					url_data = swy(path)
					print('[*]Start of analysis')
					try:
						min_tps = int(sys.argv[arg + 1])
					except:
						old(url_data)
					else:
						old(url_data, min_tps)
				elif sys.argv[arg] == '-d':
					from .src.thread import dead
					url_data = swy(path)
					print('[*]Start of analysis')
					dead(url_data)
				elif sys.argv[arg] == '-m':
					analyze = True
					if sys.argv[arg + 1] in ['html', 'raw', 'list', 'view', 'json']:
						mode = sys.argv[arg + 1]
					else:
						exit('[!] Mode file invalid')
				elif sys.argv[arg] == '-t':
					analyze = True
					try:
						count = int(sys.argv[arg + 1])
						if count == -1:
							all_time = True
					except:
						exit('[!] Numbers of day invalid')
				elif sys.argv[arg] == '-a':
					if len(sys.argv) != arg + 2:
						add_sub({sys.argv[arg+1]: [sys.argv[arg + 2]]}, path)
					else:
						exit('[!] You Forgot An Argument (-a)')
				elif sys.argv[arg] == '-l':
					analyze = True
					analyze_only_one = True
					del_data(path, False)
					if arg + 2 >= len(sys.argv):
						exit('[!] You forgot an argument after -l')
					else:
						url_data = {sys.argv[arg+1]: [sys.argv[arg+2]]}
				elif sys.argv[arg] == '-r':
					del_data(path, True)
				elif sys.argv[arg] == '-s':
					try:
						if check_id(sys.argv[arg+1]):
							from .src.thread import stat
							stat(sys.argv[arg+1])
						elif sys.argv[arg+1] == 'all':
							from .src.thread import stats
							subs = swy(path, 1)
							stats(subs)
						else:
							exit("[!] Id is not available")
					except IndexError:
						exit("[!] Missing argument after the '-s'")
				elif sys.argv[arg] == '-h':
					exit("[!] -h don't work with other options")
				elif sys.argv[arg] == '-1':
					pass
				else:
					exit("[!] No such option: {}".format(sys.argv[arg]))
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
				elif sys.argv[arg] == '--html':
					method = '1'
					analyze = True
				elif sys.argv[arg] == '--css':
					try:
						os.mkdir('css')
					except:
						print_debug('[!] CSS folder already exist or can\'t be created')
					if len(sys.argv) != arg + 1:
						write_css(sys.argv[arg+1])
					else:
						write_css('')
				elif sys.argv[arg] == '--init':
					init_swy(path, arg)
				elif sys.argv[arg] == '--ultra-html':
					method = '2'
					analyze = True
				elif sys.argv[arg] == '--loading':
					loading = True
					analyze = True
				elif sys.argv[arg] == '--output':
					if arg + 1 >= len(sys.argv):
						exit('[!] You forgot an argument after --output')
					output = sys.argv[arg+1]
					analyze = True
				elif sys.argv[arg] == '--help':
					exit("[!] -h don't work with other options")
				elif sys.argv[arg] == '--debug':
					pass
				else:
					exit("[!] No such option: {}".format(sys.argv[arg]))
	if analyze:
		passe = time.time()
		if not analyze_only_one:
			url_data = swy(path, 0)
		if output == '':
			if mode == 'html':
				output = 'sub.html'
			elif mode == 'list':
				output = 'sub_list'
			elif mode == 'raw':
				output = 'sub_raw'
			elif mode == 'json':
				output = 'sub.json'
		file = Write_file(output, path, mode, method)
		if mode == 'html':
			file.html_init()
		elif mode == 'json':
			file.json_init()
		elif mode in ['list', 'raw', 'view']:
			if os.path.exists(output):
				os.remove(output)
		nb_new = Run_analyze(url_data, output, lcl_time(int(count/30+(30-count%30)/30), all_time), path, mode, loading, file, method)
		file.sort_file(count)
		write_log(sys.argv, path, passe)
	print_debug('[*] Done')

