import re
import time
import os
import sys
import optparse

from .write import (
	Write_file,
	write_css,
	write_log
)
from .thread import (
	Run_analyze,
	old,
	dead
)
from .swy import (
	swy,
	generate_swy,
	add_sub,
	add_suburl,
	init_swy
)
from .tools import (
	del_data,
	log,
	exit_debug
)
from ..version import __version__
from ..analyzer.imports import UrlToAnalyzer


class Commands():
	def __init__(self, path):
		self.params = {
			'-a':           {'func': self._a,           'option': 'URL',    'description': "Add a sub to your sub list."},
			'-e':           {'func': self._e,           'option': '',       'description': "Edit your sub list."},
			'-h':           {'func': self._h,           'option': '',       'description': "Print this help text and exit."},
			'-l':           {'func': self._l,           'option': 'URL',    'description': "Analyze only one sub."},
			'-m':           {'func': self._m,           'option': 'MODE',   'description': "Choose the type of the output file (html, json, raw, list)."},
			'-r':           {'func': self._r,           'option': '',       'description': "Remove the cache."},
			'-t':           {'func': self._t,           'option': 'DAYS',   'description': "Select how many DAYS ago the last content written to your file will be dated ."},
			'-v':           {'func': self.nothing,      'option': '',       'description': "Verbose."},
			'--af':         {'func': self.__af,         'option': 'FILE',   'description': "Add a list of sub to your sub list."},
			'--ax':         {'func': self.__ax,         'option': 'FILE',   'description': "Add a xml file in your sub list."},
			'--cat':        {'func': self.__cat,        'option': '',       'description': "View your subscriptions."},
			'--css':        {'func': self.__css,        'option': 'STYLE',  'description': "Export the css files (light, dark, switch)."},
			'--dead':       {'func': self.__dead,       'option': '',       'description': "Show the dead channels + those who posted no videos."},
			'--help':       {'func': self._h,           'option': '',       'description': "Print this help text and exit."},
			'--html':       {'func': self.__html,       'option': '',       'description': "Recover sub with html page instead of RSS. This method recover more video."},
			'--init':       {'func': self.__init,       'option': 'FILE',   'description': "Remove all your subs and add new."},
			'--loading':    {'func': self.__loading,    'option': '',       'description': "Print a progress bar."},
			'--old':        {'func': self.__old,        'option': 'MONTHS', 'description': "Show channels who didn\'t post videos since MONTHS + dead channels."},
			'--output':     {'func': self.__output,     'option': 'FILE',   'description': "Write the output in FILE."},
			'--ultra-html': {'func': self.__ultra_html, 'option': '',       'description': "An advanced version of --html."},
			'--version':    {'func': self.__version,    'option': '',       'description': "Print version."},
		}
		self.analyze  = True
		self.count    = 7
		self.loading  = False
		self.method   = '0'
		self.mode     = 'html'
		self.output   = ''
		self.path     = path
		self.trun     = time.time()
		self.url_data = {}

	def _h(self):
		print('Usage: youtube-sm [OPTIONS]')
		print()
		print('Options:')
		for name in self.params:
				param = self.params[name]
				print('  {:12} {:8}  {}'.format(name, param['option'], param['description']))
		exit()

	def _m(self, arg):
		if arg + 1 < len(sys.argv) and sys.argv[arg + 1] in ['html', 'raw', 'list', 'view', 'json']:
			self.mode = sys.argv[arg + 1]
		else:
			exit_debug('Mode file invalid', 1)

	def _t(self, arg):
		if not re.match('(-|)[0-9]*$', sys.argv[arg + 1]):
			exit_debug('Numbers of day invalid', 1)
		self.count = int(sys.argv[arg + 1])

	def _a(self, arg):
		self.analyze = False
		if arg + 1 < len(sys.argv):
			add_suburl(sys.argv[arg+1], self.path)
		else:
			exit_debug('You Forgot An Argument (-a)', 1)

	def _e(self, arg):
		self.analyze = False
		editor = os.getenv('EDITOR')
		if editor is None:
			log.RWarning('The variable `EDITOR` is not set. `vi` is use by default')
			editor = '/bin/vi'
		os.system('{} {}sub.swy'.format(editor, self.path))

	def _l(self, arg):
		del_data(self.path)
		if arg + 1 < len(sys.argv):
			analyzer = UrlToAnalyzer(sys.argv[arg+1])
			if analyzer is None:
				log.Error('URL does not match with any site')
				exit()
			self.url_data = {analyzer.SITE: [sys.argv[arg+1]]}
		else:
			exit_debug('You forgot an argument after -l', 1)

	def _r(self, arg):
		del_data(self.path)

	def __init(self, arg):
		self.analyze = False
		init_swy(self.path, arg)

	def __af(self, arg):
		self.analyze = False
		if arg + 1 < len(sys.argv) and os.path.exists(sys.argv[arg + 1]):
			add_sub(open(sys.argv[arg + 1], 'r').read().split('\n'), self.path)
		else:
			exit_debug('File not found', 1)

	def __ax(self, arg):
		self.analyze = False
		if arg + 1 < len(sys.argv) and os.path.exists(sys.argv[arg + 1]):
			generate_swy(sys.argv[arg + 1], self.path)
		else:
			exit_debug('File not found', 1)

	def __cat(self, arg):
		self.analyze = False
		if os.path.exists(self.path + 'sub.swy'):
			with open(self.path + 'sub.swy', 'r') as file:
				while True:
					line = file.readline()
					if line == '':
						break
					print(line, end='')

	def __html(self, arg):
		self.method = '1'

	def __old(self, arg):
		self.analyze = False
		self.url_data = swy(self.path)
		log.RInfo('[*]Start of analysis')
		if re.match('[0-9]*$', sys.argv[arg + 1]):
			min_tps = int(sys.argv[arg + 1])
			old(self.url_data, min_tps)
		else:
			old(self.url_data)

	def __dead(self, arg):
		self.analyze = False
		self.url_data = swy(self.path)
		log.RInfo('Start of analysis')
		dead(self.url_data)

	def __css(self, arg):
		self.analyze = False
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

	def __loading(self, arg):
		self.loading = True

	def __output(self, arg):
		if arg + 1 >= len(sys.argv):
			exit_debug('You forgot an argument after --output', 1)
		self.output = sys.argv[arg+1]

	def __version(self, arg):
		log.RInfo('Version: {}'.format(__version__))

	def nothing(self, arg):
		pass

	def parser(self):
		if sys.argv == ['-h'] or sys.argv == ['--help']:
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
			if self.url_data == {}:
				self.url_data = swy(self.path, 0)
			file = Write_file(self.output, self.path, self.mode, self.method, self.count)
			Run_analyze(self.url_data, self.loading, file, self.method)
			file.write()
			write_log(sys.argv, self.path, self.trun)
		log.Info('Done ({} seconds)'.format(str(time.time() - self.trun)[:7]))
