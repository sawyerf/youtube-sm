import re
import time
import os
import sys
import optparse

from .test import TestAnalyzer
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
			'-c':		{'func': self._c,           'option': 'NAME',   'description': "Custom Feed"},
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
			'--old':        {'func': self.__old,        'option': '',       'description': "Show channels who didn\'t post videos since DAYS."},
			'--output':     {'func': self.__output,     'option': 'FILE',   'description': "Write the output in FILE."},
			'--version':    {'func': self.__version,    'option': '',       'description': "Print version."},
			'--test':       {'func': self.__test,       'option': '',       'description': ""},
		}
		self.exec     = 'analyze'
		self.since    = None
		self.after    = 7
		self.loading  = False
		self.method   = '0'
		self.mode     = 'html'
		self.output   = None
		self.path     = path
		self.trun     = time.time()
		self.url_data = None
		self.isarg    = False
		self.feed     = 'sub'

	def _h(self, arg):
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
			self.isarg = True
		else:
			exit_debug('Mode file invalid', 1)

	def _t(self, arg):
		if re.match('(-|)[0-9]*$', sys.argv[arg + 1]):
			self.since = int(sys.argv[arg + 1])
			self.after = self.since
		elif re.match('(-|)[0-9]*,(-|)[0-9]*$', sys.argv[arg + 1]):
			i = sys.argv[arg + 1].split(',')
			self.since = int(i[0])
			self.after = int(i[1])
		else:
			exit_debug('Numbers of day invalid', 1)
		self.isarg = True

	def _a(self, arg):
		self.exec = None
		if arg + 1 < len(sys.argv):
			add_suburl(sys.argv[arg+1], self.path, self.feed)
			self.isarg = True
		else:
			exit_debug('You Forgot An Argument (-a)', 1)

	def _c(self, arg):
		if not re.match(r'^[a-zA-Z_-]*$', sys.argv[arg+1]):
			exit_debug('Wrong Format of Feed Name (-c)', 1)
		self.feed = sys.argv[arg+1]
		self.isarg = True
		log.Info('Feed: ' + self.feed)
		if not os.path.exists(self.path + self.feed + '.swy'):
			log.Warning('`{}` Feed do not exist'.format(self.feed), 1)
		
	def _e(self, arg):
		self.exec = None
		editor = os.getenv('EDITOR')
		if editor is None:
			log.RWarning('The variable `EDITOR` is not set. `vi` is use by default')
			editor = '/bin/vi'
		os.system('{} {}{}.swy'.format(editor, self.path, self.feed))

	def _l(self, arg):
		del_data(self.path)
		if arg + 1 < len(sys.argv):
			analyzer = UrlToAnalyzer(sys.argv[arg+1])
			if analyzer is None:
				log.Error('URL does not match with any site')
				exit()
			self.url_data = {analyzer.SITE: [sys.argv[arg+1]]}
			self.path = None
			self.isarg = True
		else:
			exit_debug('You forgot an argument after -l', 1)

	def _r(self, arg):
		del_data(self.path)

	def __init(self, arg):
		self.exec = None
		init_swy(self.path, arg, self.feed)

	def __af(self, arg):
		self.exec = None
		if arg + 1 < len(sys.argv) and os.path.exists(sys.argv[arg + 1]):
			add_sub(open(sys.argv[arg + 1], 'r').read().split('\n'), self.path, self.feed)
			self.isarg = True
		else:
			exit_debug('File not found', 1)

	def __ax(self, arg):
		self.exec = None
		if arg + 1 < len(sys.argv) and os.path.exists(sys.argv[arg + 1]):
			generate_swy(sys.argv[arg + 1], self.path, self.feed)
			self.isarg = True
		else:
			exit_debug('File not found', 1)

	def __cat(self, arg):
		self.exec = None
		if os.path.exists(self.path + self.feed + '.swy'):
			with open(self.path + self.feed + '.swy', 'r') as file:
				while True:
					line = file.readline()
					if line == '':
						break
					print(line, end='')

	def __html(self, arg):
		self.method = '1'

	def __old(self, arg):
		self.exec = 'old'

	def __dead(self, arg):
		self.exec = 'dead'

	def __css(self, arg):
		self.exec = None
		try:
			os.mkdir('css')
		except:
			log.Error('CSS folder already exist or can\'t be created')
		if len(sys.argv) != arg + 1:
			write_css(sys.argv[arg+1])
			self.isarg = True
		else:
			write_css('')

	def __loading(self, arg):
		self.loading = True

	def __output(self, arg):
		if arg + 1 >= len(sys.argv):
			exit_debug('You forgot an argument after --output', 1)
		self.output = sys.argv[arg+1]
		self.isarg = True

	def __test(self, arg):
		self.exec = 'test'

	def __version(self, arg):
		log.RInfo('Version: {}'.format(__version__))

	def nothing(self, arg):
		pass

	def parser(self):
		for arg in range(len(sys.argv)):
			if self.isarg:
				self.isarg = False
			elif sys.argv[arg] in self.params:
				self.params[sys.argv[arg]]['func'](arg)
			else:
				exit_debug("No such option: `{}`".format(sys.argv[arg]), 1)

	def router(self):
		if self.url_data is None:
			self.url_data = swy(self.path, 0, self.feed)
		if self.exec == 'analyze':
			if self.since is None:
				self.since = 7
			file = Write_file(self.output, self.path, self.mode, self.method, self.since, self.after, self.feed)
			Run_analyze(self.url_data, self.loading, file, self.method)
			file.write()
			write_log(sys.argv, self.path, self.trun)
		elif self.exec == 'old':
			if self.since is None:
				self.since = 365
			old(self.url_data, self.since)
		elif self.exec == 'dead':
			dead(self.url_data)
		elif self.exec == 'test':
			TestAnalyzer(self.path)
		log.Info('Done ({} seconds)'.format(str(time.time() - self.trun)[:7]))
