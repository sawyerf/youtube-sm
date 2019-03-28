import time
import os
import sys

from ..src.write import (
	Write_file,
	write_css,
	write_log)
from ..src.thread import (
	Run_analyze,
	old,
	dead)
from ..src.swy import (
	swy,
	generate_swy,
	add_sub,
	init_swy)
from ..src.tools import (
	del_data,
	check_id,
	print_debug)
from ..src.time import lcl_time

class	Commands():
	def __init__(self, path):
		self.url_data = []
		self.analyze = False
		self.analyze_only_one = False
		self.loading = False
		self.method = '0'
		self.mode = 'html'
		self.count = 7
		self.all_time = False
		self.output = ''
		self.sub_file = 'subscription_manager'
		self.site = 'youtube'
		self.path = path
		self.passe = 0

	def parser(self):
		if sys.argv == []: # Default command
			self.passe = time.time()
			self.url_data = swy(self.path)
			file = Write_file('sub.html', self.path, 'html', '0')
			file.html_init()
			Run_analyze(self.url_data, 'sub.html', lcl_time(), self.path, 'html', False, file, '0')
			file.html_json_end()
			write_log(sys.argv, self.path, self.passe)
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
				if len(sys.argv[0]) > 0 and sys.argv[arg][0] != '-':
					continue
				if len(sys.argv[0]) > 1 and sys.argv[arg][1] != '-':
					if sys.argv[arg] == '-o':
						self.url_data = swy(self.path)
						print('[*]Start of analysis')
						try:
							min_tps = int(sys.argv[arg + 1])
						except:
							old(self.url_data)
						else:
							old(self.url_data, min_tps)
					elif sys.argv[arg] == '-d':
						self.url_data = swy(self.path)
						print('[*]Start of analysis')
						dead(self.url_data)
					elif sys.argv[arg] == '-m':
						self.analyze = True
						if sys.argv[arg + 1] in ['html', 'raw', 'list', 'view', 'json']:
							self.mode = sys.argv[arg + 1]
						else:
							exit('[!] Mode file invalid')
					elif sys.argv[arg] == '-t':
						self.analyze = True
						try:
							self.count = int(sys.argv[arg + 1])
							if self.count == -1:
								self.all_time = True
						except:
							exit('[!] Numbers of day invalid')
					elif sys.argv[arg] == '-a':
						if len(sys.argv) != arg + 2:
							add_sub({sys.argv[arg+1]: [sys.argv[arg + 2]]}, self.path)
						else:
							exit('[!] You Forgot An Argument (-a)')
					elif sys.argv[arg] == '-l':
						self.analyze = True
						self.analyze_only_one = True
						del_data(self.path, False)
						if arg + 2 >= len(sys.argv):
							exit('[!] You forgot an argument after -l')
						else:
							self.url_data = {sys.argv[arg+1]: [sys.argv[arg+2]]}
					elif sys.argv[arg] == '-r':
						del_data(self.path, True)
					elif sys.argv[arg] == '-s':
						try:
							if sys.argv[arg+1] == 'all':
								from .src.thread import stats
								subs = swy(self.path, 1)
								stats(subs)
							else:
								from .src.thread import stats
								stats({sys.argv[arg+1]: {sys.argv[arg+2]: sys.argv[arg+2]}})
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
							add_sub(open(sys.argv[arg + 1], 'r').read().split('\n'), self.path)
						else:
							exit('[!] File not found')
					elif sys.argv[arg] == '--ax':
						if os.path.exists(sys.argv[arg + 1]):
							generate_swy(sys.argv[arg + 1], self.path)
						else:
							exit('[!] File not found')
					elif sys.argv[arg] == '--cat':
						if os.path.exists(self.path + 'sub.swy'):
							with open(self.path + 'sub.swy', 'r') as file:
								while True:
									line = file.readline()
									if line == '':
										break
									try:
										print(line, end='')
									except:
										print(line.encode())
					elif sys.argv[arg] == '--html':
						self.method = '1'
						self.analyze = True
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
						init_swy(self.path, arg)
					elif sys.argv[arg] == '--ultra-html':
						self.method = '2'
						self.analyze = True
					elif sys.argv[arg] == '--loading':
						self.loading = True
						self.analyze = True
					elif sys.argv[arg] == '--output':
						if arg + 1 >= len(sys.argv):
							exit('[!] You forgot an argument after --output')
						self.output = sys.argv[arg+1]
						self.analyze = True
					elif sys.argv[arg] == '--help':
						exit("[!] -h don't work with other options")
					elif sys.argv[arg] == '--debug':
						pass
					else:
						exit("[!] No such option: {}".format(sys.argv[arg]))
	
	def	router(self):
		if self.analyze:
			self.passe = time.time()
			if not self.analyze_only_one:
				self.url_data = swy(self.path, 0)
			if self.output == '':
				if self.mode == 'html':
					self.output = 'sub.html'
				elif self.mode == 'list':
					self.output = 'sub_list'
				elif self.mode == 'raw':
					self.output = 'sub_raw'
				elif self.mode == 'json':
					self.output = 'sub.json'
			file = Write_file(self.output, self.path, self.mode, self.method)
			if self.mode == 'html':
				file.html_init()
			elif self.mode == 'json':
				file.json_init()
			elif self.mode in ['list', 'raw', 'view']:
				if os.path.exists(self.output):
					os.remove(self.output)
			nb_new = Run_analyze(self.url_data, self.output, lcl_time(int(self.count/30+(30-self.count%30)/30), self.all_time), self.path, self.mode, self.loading, file, self.method)
			file.sort_file(self.count)
			write_log(sys.argv, self.path, self.passe)
		print_debug('[*] Done')
