import time
import os
import sys
from .src.analyzer import (
	html_init,
	html_end,
	init,
	sort_file)
from .src.swy import (
	swy,
	generate_swy,
	add_sub)
from .src.tools import (
	del_data,
	check_id)
from .src.time import lcl_time



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
	method = '0'
	mode = 'html'
	count = 7
	all_time = False
	output = ''
	sub_file = 'subscription_manager'
	#path
	if os.name == 'nt':
		path = os.path.expanduser('~') + '/.youtube_sm/'
	else:
		if os.uname().sysname == 'Linux' or os.uname().sysname == 'Darwin':
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
		init(url_data, 'sub.html', lcl_time(), path)
		html_end(path=path)
		open(path + 'log', 'a').write(str(time.time() - passe) + '\t' + time.strftime("%H%M") + '\n')
	elif sys.argv == ['-h'] or sys.argv == ['--help']:
		print("""Usage: youtube-sm [OPTIONS]

Options:
   -h                     Print this help text and exit
   -n     [file]          Use an other xml file for your subscriptions
   -m     [mode]          Choose the type of the output (html, raw, list, view)
   -t     [nb of days]    Choose how far in the past do you want the program to look for videos
   -d                     Show the dead channels + those who posted no videos
   -o     [nb of months]  Show the channels who didn't post videos in [nb of months] + dead channels
   -l     [id]            Analyze only one channel or playlist
   -r                     Remove the cache
   -s     [id/all]        Outputs the stats of the selected channel(s)
   -a     [id]            Append a channel or a playlist at the end of sub.
   --init [file]          Remove all your subs and the cache and init with your subscription file.
   --af   [file]          Append a file with list of channel or a playlist in sub.swy
   --ax   [file]          Append a xml file in sub.swy
   --html                 Recover yours subs in the common page web (more videos)
   --ultra-html           Recover all the videos with the common page and the button 'load more'
   --output [file]        Choose the name of the output file
   --cat                  View your subscriptions
   --css                  Import the css files
   --loading              Prints a progress bar while running
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
					if sys.argv[arg + 1] in ['html', 'raw', 'list', 'view']:
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
					del_data(path, False)
					if arg + 1 >= len(sys.argv):
						exit('[!] You forgot an argument after -l')
					if sys.argv[arg + 1][:2] in ['UC', 'PL']:
						url_data = [sys.argv[arg + 1]]
					else:
						exit('[!] Id is not available')
				elif sys.argv[arg] == '-r':
					del_data(path, True)
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
						pass
					open('css/sub.css', 'a', encoding='utf8').write(".left\n{\n	float: left;\n	\n}\n.clear\n{\n	clear: both;\n}\n*\n{\n	font-family: Arial;\n}\n\ndiv\n{\n	margin: 10px 27% 10px 27%;\n}\nimg\n{\n	width: 280px;\n	height: 157px;\n	margin-right: 7px;\n}\nh4\n{\n	line-height: 18px;\n	font-size: 18px;\n	margin: 0px 0px -5px 0px;\n}\np\n{\n	color: grey;\n	line-height: 7px;\n}\na\n{\n	text-decoration: none;\n	color: black;\n}\n")
					open('css/sub_mobile.css', 'a', encoding='utf8').write(".left\n{\n	float:left;\n}\n.clear\n{\n	clear: both;\n}\n*\n{\n	font-family: Arial;\n}\ndiv\n{\n	margin-left: 0%;\n	margin-right: 0%;\n	margin: 10px 0px 10px 0px;\n}\nimg\n{\n	width: 380px;\n	height: 214px;\n}\nh4\n{\n	line-height: 30px;\n	font-size: 30px;\n	margin: 0px 0px -10px 0px;\n}\np\n{\n	color: grey;\n	line-height: 5px;\n	font-size: 1.9em;\n}\na\n{\n	text-decoration: none;\n	color: black;\n}")
				elif sys.argv[arg] == '--init':
					init_command(path, arg)
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
				else:
					exit("[!] No such option: {}".format(sys.argv[arg]))
	if analyze:
		passe = time.time()
		if not analyze_only_one:
			url_data = swy(sub_file, path=path)
		if output == '':
			if mode == 'html':
				output = 'sub.html'
			elif mode == 'list':
				output = 'sub_list'
			elif mode == 'raw':
				output = 'sub_raw'
		if mode == 'html':
			html_init(path, output)
		elif mode == 'raw' or mode == 'list':
			if os.path.exists(output):
				os.remove(output)			
		nb_new = init(url_data, output, lcl_time(int(count/30+(30-count%30)/30), all_time), path, mode, loading, method)
		sort_file(count, output, mode, path, method)
		open(path + 'log', 'a').write(str(time.time() - passe) + '\t' + time.strftime("    %H%M") + '\n')
