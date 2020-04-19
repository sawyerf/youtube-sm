import re
import time
import os
import sys

from .write import (
	Write_file,
	write_css,
	write_log)
from .thread import (
	Run_analyze,
	old,
	stats,
	dead)
from .swy import (
	swy,
	generate_swy,
	add_sub,
	add_suburl,
	init_swy)
from .tools import (
	del_data,
	log,
	exit_debug)
from .time import lcl_time
from ..version	import __version__
from ..analyzer.imports import UrlToAnalyzer

class Commands():
	def __init__(self, path):
		self.params = {
			'-a':			{'func': self._a,			'option': 'URL',		'description': "Add a sub to your sub list."},
			'-e':			{'func': self._e,			'option': '',			'description': "Edit your sub list."},
			'-h':			{'func': self._h,			'option': '',			'description': "Print this help text and exit."},
			'-l':			{'func': self._l,			'option': 'URL',		'description': "Analyze only one sub."},
			'-m':			{'func': self._m,			'option': 'MODE',		'description': "Choose the type of the output file (html, json, raw, list, view)."},
			'-r':			{'func': self._r,			'option': '',			'description': "Remove the cache."},
			'-s':			{'func': self._s,			'option': 'URL',		'description': "Stats of the selected channel(s)."},
			'-t':			{'func': self._t,			'option': 'DAYS',		'description': "Select how many DAYS ago the last content written to your file will be dated ."},
			'-v':			{'func': self.nothing,		'option': '',			'description': "Verbose."},
			'--af':			{'func': self.__af,			'option': 'FILE',		'description': "Add a list of sub to your sub list."},
			'--ax':			{'func': self.__ax,			'option': 'FILE',		'description': "Add a xml file in your sub list."},
			'--cat':		{'func': self.__cat,		'option': '',			'description': "View your subscriptions."},
			'--css':		{'func': self.__css,		'option': 'STYLE',		'description': "Export the css files (light, dark, switch)."},
			'--dead':		{'func': self.__dead,		'option': '',			'description': "Show the dead channels + those who posted no videos."},
			'--help':		{'func': self._h,			'option': '',			'description': "Print this help text and exit."},
			'--html':		{'func': self.__html,		'option': '',			'description': "Recover sub with html page instead of RSS. This method recover more video."},
			'--init':		{'func': self.__init,		'option': 'FILE',		'description': "Remove all your subs and add new."},
			'--loading':	{'func': self.__loading,	'option': '',			'description': "Print a progress bar."},
			'--old':		{'func': self.__old,		'option': 'MONTHS',		'description': "Show channels who didn\'t post videos since MONTHS + dead channels."},
			'--output':		{'func': self.__output,		'option': 'FILE',		'description': "Write the output in FILE."},
			'--ultra-html':	{'func': self.__ultra_html,	'option': '',			'description': "An advanced version of --html."},
			'--version':	{'func': self.__version,	'option': '',			'description': "Print version."},
		}
		self.url_data = []
		self.analyze = False
		self.analyze_only_one = False
		self.loading = False
		self.method = '0'
		self.mode = 'html'
		self.count = 7
		self.all_time = False
		self.output = ''
		self.path = path
		self.trun = time.time()

	def _h(self):
		print('Usage: youtube-sm [OPTIONS]')
		print()
		print('Options:')
		for name in self.params:
				param = self.params[name]
				print('  {:12} {:8}  {}'.format(name, param['option'], param['description']))
		exit()

	def _m(self, arg):
		self.analyze = True
		if arg + 1 < len(sys.argv) and sys.argv[arg + 1] in ['html', 'raw', 'list', 'view', 'json']:
			self.mode = sys.argv[arg + 1]
		else:
			exit_debug('Mode file invalid', 1)

	def _t(self, arg):
		self.analyze = True
		try:
			self.count = int(sys.argv[arg + 1])
			if self.count == -1:
				self.all_time = True
		except:
			exit_debug('Numbers of day invalid', 1)

	def _a(self, arg):
		if re.match('\[.*\]', sys.argv[arg+1]) and arg + 2 < len(sys.argv):
			add_sub({sys.argv[arg+1]: [sys.argv[arg + 2]]}, self.path)
		elif arg + 1 < len(sys.argv):
			add_suburl(sys.argv[arg+1], self.path)
		else:
			exit_debug('You Forgot An Argument (-a)', 1)

	def _e(self, arg):
		editor = os.getenv('EDITOR')
		if editor == None:
			self.RWarning('The variable `EDITOR` is not set. `vi` is use by default')
			editor = '/bin/vi'
		os.system('{} {}sub.swy'.format(editor, self.path))

	def _l(self, arg):
		self.analyze = True
		self.analyze_only_one = True
		del_data(self.path, False)
		if re.match('\[.*\]', sys.argv[arg+1]) and arg + 2 < len(sys.argv):
			self.url_data = {sys.argv[arg+1]: [sys.argv[arg+2]]}
		elif arg + 1 < len(sys.argv):
			analyzer = UrlToAnalyzer(sys.argv[arg+1])
			self.url_data = {analyzer.SITE: [sys.argv[arg+1]]}
		else:
			exit_debug('You forgot an argument after -l', 1)

	def _s(self, arg):
		try:
			if sys.argv[arg+1] == 'all':
				subs = swy(self.path, 1)
				stats(subs)
			else:
				stats({sys.argv[arg+1]: {sys.argv[arg+2]: sys.argv[arg+2]}})
		except IndexError:
			exit_debug("Missing argument after the '-s'", 1)

	def _r(self, arg):
		del_data(self.path, True)

	def __init(self, arg):
		init_swy(self.path, arg)

	def __af(self, arg):
		if arg + 1 < len(sys.argv) and os.path.exists(sys.argv[arg + 1]):
			add_sub(open(sys.argv[arg + 1], 'r').read().split('\n'), self.path)
		else:
			exit_debug('File not found', 1)

	def __ax(self, arg):
		if arg + 1 < len(sys.argv) and os.path.exists(sys.argv[arg + 1]):
			generate_swy(sys.argv[arg + 1], self.path)
		else:
			exit_debug('File not found', 1)

	def __cat(self, arg):
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

	def __html(self, arg):
		self.method = '1'
		self.analyze = True

	def __old(self, arg):
		self.url_data = swy(self.path)
		self.RInfo('[*]Start of analysis')
		try:
			min_tps = int(sys.argv[arg + 1])
		except:
			old(self.url_data)
		else:
			old(self.url_data, min_tps)

	def __dead(self, arg):
		self.url_data = swy(self.path)
		self.RInfo('Start of analysis')
		dead(self.url_data)

	def __css(self, arg):
		try:
			os.mkdir('css')
		except:
			log.Error('CSS folder already exist or can\'t be created')
		if len(sys.argv) != arg + 1:
			write_css(sys.argv[arg+1])
		else:
			write_css('')

	def __ultra_html(self, arg):
		self.method = '2'
		self.analyze = True

	def __loading(self, arg):
		self.loading = True
		self.analyze = True

	def __output(self, arg):
		if arg + 1 >= len(sys.argv):
			exit_debug('You forgot an argument after --output', 1)
		self.output = sys.argv[arg+1]
		self.analyze = True

	def __version(self, arg):
		log.RInfo('Version: {}'.format(__version__))

	def __default(self):
		self.url_data = swy(self.path)
		file = Write_file('sub.html', self.path, 'html', '0')
		file.html_init()
		Run_analyze(self.url_data, 'sub.html', lcl_time(), self.path, 'html', False, file, '0')
		file.html_json_end()
		write_log(sys.argv, self.path, self.trun)

	def nothing(self, arg):
		pass

	def parser(self):
		if sys.argv in [[], ['-v']]: # Default command
			self.__default()
		elif sys.argv == ['-h'] or sys.argv == ['--help']:
			self._h()
		else:
			for arg in range(len(sys.argv)):
				if len(sys.argv[arg]) == 0 or sys.argv[arg][0] != '-' or sys.argv[arg] == '-1':
					continue
				elif len(sys.argv[arg]) > 1:
					if sys.argv[arg] in self.params:
						self.params[sys.argv[arg]]['func'](arg)
					else:
						exit_debug("No such option: {}".format(sys.argv[arg]), 1)

	def router(self):
		if self.analyze:
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
			nb_new = Run_analyze(self.url_data, self.output, lcl_time(self.count + 30, self.all_time), self.path, self.mode, self.loading, file, self.method)
			file.sort_file(self.count)
			write_log(sys.argv, self.path, self.trun)
		log.Info('Done ({} seconds)'.format(str(time.time() - self.trun)[:7]))
