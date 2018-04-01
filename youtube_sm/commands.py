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

def init_command(path, arg):
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
		if add_file[len(add_file) - 4:] == '.swy':
			with open(add_file, 'rb') as file, open(path + 'sub.swy', 'a', encoding='utf8') as sub_file:
				nb_line = 1
				while True:
					line = file.readline().decode('utf8')
					if '\t' in line:
						sub_file.write(line)
					elif line == '':
						break
					else:
						print('[!] No tabs in line ' + str(nb_line))
		else:
			url_data = swy(add_file, path=path)
	else:
		if os.path.exists('subscription_manager'):
			url_data = swy('subscription_manager', path=path)
		else:
			exit('[!] File Not Found (subscription_manager)')
	print('[*] Subs append to sub.swy')
	exit('[*] Done')

def main():
	url_data = []
	analyze = False
	analyze_only_one = False
	loading = False
	mode = 'html'
	count = 7
	all_time = False
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
   -h                     Print this help text and exit
   -n     [file]          To use an other xml file for yours subscriptions
   -m     [mode]          The type of file do you want (html, raw, list)
   -t     [nb of days]    Numbers of days of subscriptions do you want in your file
   -d                     Show the dead channels + those who posted no videos
   -o     [nb of months]  Show the channels who didn't post videos in nb of months + dead channels
   -l     [id]            If you want to analyze only one channel or playlist
   -r                     To remove the cache before analyze
   -s     [id/all]        To have the stat of the channel(s)
   -a     [id]            To append a channel or a playlist at the end of sub.
   --init [file]          Remove all your subs and the cache and init with your subscription file.
   --af   [file]          To append a file with list of channel or a playlist in sub.swy
   --ax   [file]          To append a xml file in sub.swy
   --cat                  To read 'sub.swy'
   --css                  Import the css files
   --loading              To print a progress bar
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
						if count == -1:
							all_time = True
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
						try:
							os.makedirs(path + 'data/')
						except:
							pass
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
				elif sys.argv[arg] == '--css':
					try:
						os.mkdir('css')
					except:
						pass
					open('css/sub.css', 'a', encoding='utf8').write(".left\n{\n	float: left;\n	\n}\n.clear\n{\n	clear: both;\n}\n*\n{\n	font-family: Arial;\n}\n\ndiv\n{\n	margin: 10px 27% 10px 27%;\n}\nimg\n{\n	width: 280px;\n	height: 157px;\n	margin-right: 7px;\n}\nh4\n{\n	line-height: 18px;\n	font-size: 18px;\n	margin: 0px 0px -5px 0px;\n}\np\n{\n	color: grey;\n	line-height: 7px;\n}\na\n{\n	text-decoration: none;\n	color: black;\n}\n")
					open('css/sub_mobile.css', 'a', encoding='utf8').write(".left\n{\n	float:left;\n}\n.clear\n{\n	clear: both;\n}\n*\n{\n	font-family: Arial;\n}\ndiv\n{\n	margin-left: 0%;\n	margin-right: 0%;\n	margin: 10px 0px 10px 0px;\n}\nimg\n{\n	width: 380px;\n	height: 214px;\n}\nh4\n{\n	line-height: 30px;\n	font-size: 30px;\n	margin: 0px 0px -10px 0px;\n}\np\n{\n	color: grey;\n	line-height: 5px;\n	font-size: 1.9em;\n}\na\n{\n	text-decoration: none;\n	color: black;\n}")
				elif sys.argv[arg] == '--init':
					init_command(path, arg)
				elif sys.argv[arg] == '--loading':
					loading = True
					analyze = True
	if analyze:
		passe = time.time()
		if not analyze_only_one:
			url_data = swy(sub_file, path=path)
		if mode == 'html':
			html_init(path)
			nb_new = init(url_data, lcl_time(int(count/30+(30-count%30)/30), all_time), path, mode, loading)
			html_end(count, path)
		elif mode == 'raw':
			if os.path.exists('sub_raw'):
				os.remove('sub_raw')
			nb_new = init(url_data, lcl_time(int(count/30+(30-count%30)/30), all_time), path, mode, loading)
			raw_end(count)
		elif mode == 'list':
			if os.path.exists('sub_list'):
				os.remove('sub_list')
			nb_new = init(url_data, lcl_time(int(count/30+(30-count%30)/30), all_time), path, mode, loading)
			list_end(count)
		open(path + 'log', 'a').write(str(time.time() - passe) + '\t' + str(nb_new) + '\t' + time.strftime("    %H%M") + '\n')
