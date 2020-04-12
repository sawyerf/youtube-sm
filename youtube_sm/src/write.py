import time
import os

from .time import since
from .tools import log
from datetime import datetime, timedelta

class Write_file():
	def __init__(self, output='sub.html', path_cache='', mode='html', method='0'):
		if output != '':
			self.output = output
		else:
			if mode == 'html':
				self.output = 'sub.html'
			elif mode == 'list':
				self.output = 'sub_list'
			elif mode == 'raw':
				self.output = 'sub_raw'
			elif mode == 'view':
				self.output = 'sub_view'
			elif mode == 'json':
				self.output = 'sub.json'
			else:
				self.output = 'sub'
		self.mode = mode
		self.method = method
		self.path_cache = path_cache # The path where the data and the sub are stock

	def write(self, url='', title='', url_channel='', url_img='', channel='', date='', data_file='', view=''):
		"""Write the information in a file"""
		if self.mode == 'html':
			return self.append_html(url, title, url_channel, url_img, channel, date, data_file)
		elif self.mode == 'raw':
			return self.append_raw(url, title, url_channel, url_img, channel, date, data_file)
		elif self.mode == 'list':
			return self.append_list(url, data_file)
		elif self.mode == 'view':
			return self.append_view(view)
		elif self.mode == 'json':
			return self.append_json(title, url, url_channel, channel, date, url_img, view, data_file)

	def json_init(self):
		log.Info('Init json')
		try:
			os.makedirs(self.path_cache + 'data/' + self.mode + '/' + self.method)
		except:
			log.Error('Cache folder already exist or can\'t be create')
			pass
		open(self.output, 'w', encoding='utf8').write('{\n"items" : [\n')

	def html_init(self):
		"""To init the html file"""
		log.Info('Init html')
		try:
			os.makedirs(self.path_cache + 'data/' + self.mode + '/' + self.method)
		except:
			log.Warning('Cache folder already exist or can\'t be create')
			pass
		open(self.output, 'w', encoding='utf8').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="css/sub.css" />
		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>
		<title>Abonnements</title>
	</head>
	<body>
		<!-- {} -->""".format(time.ctime()) + """
		<div class="But"><input value="" id="but" type="submit" onclick="lol()"></div>
		<div id="first"></div>
		<script type="text/javascript" src="css/button.js"></script>
""")

	def append_raw(self, url, title, url_channel, url_img, channel, date, data_file):
		"""Append the informations wich are been recover 
		in the file 'sub_raw'."""
		var = data_file[0] + data_file[1] + '\t' + date + '\t' + url + '\t' + url_channel + '\t' + title + '\t' + channel + '\t' + url_img
		if '\n' in var:
			return False
		open(self.output, 'a', encoding='utf8').write(var + '\n')
		var = ""
		return True

	def append_list(self, url, data_file):
		""""Append the informations wich are been recover
		in the file 'sub_raw'. The date is add to sort the
		videos, but it's deleted"""
		var = data_file[0] + data_file[1] + ' ' + url
		if not '\n' in var:
			open(self.output, 'a', encoding='utf8').write(var + '\n')
			return True
		else:
			return False

	def append_view(self, view):
		""" Write the views in a file"""
		if view != None:
			open(self.output, 'a', encoding='utf8').write(view + '\n')

	def append_html(self, url, title, url_channel, url_img,  channel, date, data_file):
		"""Append the informations wich are been recover
		in a file in '.../data/[date]/.' """
		try:
			data = open(self.path_c(data_file, False), 'rb+').read().decode("utf8")
			if url in data:
				return False
		except:
			try:
				os.mkdir(self.path_c(data_file, True))
			except:
				pass
		open(self.path_c(data_file, False), 'a', encoding='utf-8').write("""		<!--NEXT -->
		<div class="video">
			<a class="left" href="{}">
				<div class="container">
					<img src="{}">
					<div class="bottom-right"></div>
				</div>
			</a>
			<a href="{}"><h4>{}</h4> </a>
			<a href="{}"> <p>{}</p> </a>
			<p>{}</p>
			<p class="clear"></p>
		</div>\n""".format(url, url_img, url, title, url_channel, channel, date))
		return True

	def append_json(self, title, url, url_channel, channel, date, url_img, view, data_file):
		try:
			data = open(self.path_c(data_file, False), 'rb+').read().decode("utf8")
			if url in data:
				return False
		except:
			try:
				os.mkdir(self.path_c(data_file, True))
			except:
				pass
		open(self.path_c(data_file, False), 'a', encoding='utf8').write("{" + """
	"title": "{}",
	"id": "{}",
	"idChannel": "{}",
	"uploader": "{}",
	"uploaded": "{}",
	"image": "{}",
	"views": "{}"\n""".format(title, url, url_channel, channel, date, url_img, view) + "}\n")

	def path_c(self, data_file, folder=True):
		if folder:
			return '{}data/{}/{}/{}/'.format(self.path_cache, self.mode, self.method, data_file[0])
		else:
			return '{}data/{}/{}/{}/{}'.format(self.path_cache, self.mode, self.method, data_file[0], data_file[1])

	def sort_file(self, day=7):
		""" To sort the videos by date or add the videos in the file"""
		if self.mode == 'html' or self.mode == 'json':
			self.html_json_end(day)
		elif self.mode == 'list' or self.mode == 'raw':
			self.raw_list_end(day)

	def html_json_end(self, day=7, play=True):
		"""Recover the file in '.../data/.' with all the
		informations, sort by date and add the informations
		in './sub.html'. """
		log.Info('Start sort of {}'.format(self.mode))
		first = True
		fch = sorted(os.listdir(self.path_cache + 'data/' + self.mode + '/' + self.method + '/'))
		if len(fch) == 0:
			date		= 0
			futur_date	= 0
		elif day == -1:
			date		= -1
			futur_date	= 99999999999999
		else:
			date		= int(since(day)[:8])
			futur_date	= int(since(-1 * day)[:8])
		sub_file = open(self.output, 'a', encoding='utf-8')
		i = -1
		while True:
			i += 1
			try:
				folder_date = int(fch[-1-i])
			except IndexError:
				break
			except:
				if play:
					folder_date = 0
				else:
					continue
			if folder_date > date and folder_date < futur_date:
				fch_in = sorted(os.listdir(self.path_cache + 'data/' + self.mode + '/' + self.method + '/' + fch[-1-i]))
				for a in range(len(fch_in)):
					data = open(self.path_cache + 'data/' + self.mode + '/' + self.method + '/' + fch[-1-i] + '/' + fch_in[-1-a], 'r', encoding='utf-8').read()
					if first == False and self.mode == 'json':
						sub_file.write(',')
					else:
						first = False
					sub_file.write(data)
		sub_file.close()
		if self.mode == 'html':
			open(self.output, 'a').write('</body></html>')
		elif self.mode == 'json':
			open(self.output, 'a').write(']}')

	def raw_list_end(self, day=7):
		"""Sorted the videos by date"""
		log.Info('Start sort of {}'.format(self.mode))
		try:
			linfo = sorted(open(self.output, 'rb').read().decode('utf8').replace('\r', '').split('\n'))
		except FileNotFoundError:
			return 
		fichier = open(self.output, 'w', encoding='utf8')
		if day == -1:
			date = -1
		else:
			date = int(since(day)[:8])
		i = -1
		while True:
			i += 1
			try:
				folder_date = int(linfo[-1-i][:8])
			except IndexError:
				break
			except:
				continue
			if folder_date > date:
				fichier.write(linfo[-1-i][15:] + '\n')
			else:
				break

def write_css(arg):
	if arg == '' or arg == 'light' or arg[0] == '-':
		open('css/sub.css', 'w').write(':root {\n	--Back: white;\n	--DivHover : #e9edf3;\n	--Div: white;\n	--ColorH4: black;\n	--ColorP: grey;\n	--ColorBut: #e2e5e9;\n 	--HeightBut: 0px;\n	--HeightButMob: 0px }\n')
	elif arg == 'dark':
		open('css/sub.css', 'w').write(':root {\n	--Back: #181a1d;\n	--DivHover : #1c1e21;\n	--Div: #26292e;\n	--ColorH4: #dcdddf;\n	--ColorP: grey;\n	--ColorBut: #e2e5e9;\n	--HeightBut: 0px;\n	--HeightButMob: 0px }\n')
	elif arg == 'switch':
		open('css/button.js', 'w').write('function lol() {\n	if (lel == "1") {\n		document.documentElement.style.setProperty("--Back", "#181a1d");\n		document.documentElement.style.setProperty("--Div", "#1c1e21");\n		document.documentElement.style.setProperty("--DivHover", "#26292e");\n		document.documentElement.style.setProperty("--ColorH4", "#dcdddf");\n		document.documentElement.style.setProperty("--ColorP", "grey");\n		document.documentElement.style.setProperty("--ColorBut", "#292c30");\n		document.cookie = "lel=1";\n		lel = "2"\n	} else if (lel == "2"){\n		document.documentElement.style.setProperty("--Back", "white");\n		document.documentElement.style.setProperty("--Div", "white");\n		document.documentElement.style.setProperty("--DivHover", "white");\n		document.documentElement.style.setProperty("--ColorH4", "black");\n		document.documentElement.style.setProperty("--ColorP", "grey");\n		document.documentElement.style.setProperty("--ColorBut", "#e2e5e9");\n		document.cookie = "lel=2";\n		lel = "1"} }\ndocument.documentElement.style.setProperty("--HeightBut", "25px");\ndocument.documentElement.style.setProperty("--HeightButMob", "50px");\nif (document.cookie == ""){	var lel = "1"\n} else { lel = document.cookie.replace("lel=", "")}\nlol();')
		open('css/sub.css', 'w').write(':root {\n	--Back: white;\n	--DivHover : #e9edf3;\n	--Div: white;\n	--ColorH4: black;\n	--ColorP: grey;\n	--ColorBut: #e2e5e9;\n 	--HeightBut: 0px;\n	--HeightButMob: 0px }\n')
	else:
		exit('[!] No such argument: ' + arg)
	open('css/sub.css', 'a').write('.left { float: left; }\n.clear { clear: both; }\n* { font-family: Arial;}\n\nbody {\n\tmargin: 0 0 0 0;\n\tbackground-color: var(--Back);}\n\n.But {\n\twidth: 100%;\n\tposition: fixed;}\n\n#but {\n\t-webkit-appearance: none;\n\tborder: none;\n\tbackground-color: var(--ColorBut);\n\twidth: 100%;\n\theight: var(--HeightBut); }\n\n#first{\n\tmargin: 0 27% 0 27%;\n\theight: var(--HeightBut); }\n\ndiv.video:hover{ \n\tbackground-color: var(--DivHover); }\n\ndiv.video {\n\tbackground-color: var(--Div);\n\tmargin: 5px 27% 5px 27%; }\n\nimg {\n\twidth: 280px;\n\theight: 157px;\n\tmargin-right: 5px; }\n\nh4 {\n\tcolor: var(--ColorH4);\n\tline-height: 18px;\n\tfont-size: 18px;\n\tmargin: 0px 0px 10px 0px; }\n\np {\n\tcolor: var(--ColorP);\n\tmargin: 4px 0px 4px 0px;\n}\n\na{\n\ttext-decoration: none;\n\tcolor: black; }\n\n.description {\n\toverflow: hidden;\n\tdisplay: -webkit-box;\n\t-webkit-line-clamp: 3;\n\t-webkit-box-orient: vertical;\n  white-space: pre;\n}\n.container {\n\tposition: relative;\n\ttext-align: center;\n\tcolor: white;\n}\n\n/* Bottom right text */\n.bottom-right {\n\tposition: absolute;\n\tbackground-color: rgba(25, 25, 25, 0.5);\n\tpadding: 5 5 5 5;\n\tmargin-right: 5;\n\tbottom: 0%;\n\tright: 0%;\n}\n')
	open('css/sub_mobile.css', 'w').write('.left { float:left; }\n.clear { clear: both; }\n* { font-family: Arial; }\n\n\n.description {\n\toverflow: hidden;\n\tdisplay: -webkit-box;\n\t-webkit-line-clamp: 1;\n\t-webkit-box-orient: vertical;\n}\n#But{\n\tmargin: 0 0 0 0;\n\tposition: fixed;\n\twidth: 100%;\n}\n\n#but {\n\theight: var(--HeightButMob);\n\tmargin: 0 0 0 0;}\n\n#first{\n\tmargin: 0 0 0 0;\n\twidth: 100%;\n\theight: var(--HeightButMob);\n}\n\ndiv.video {\n\tmargin-left: 0%;\n\tmargin-right: 0%;\n\tmargin: 10px 10px 10px 10px; }\n\n\nimg {\n\twidth: 380px;\n\theight: 214px; }\n\nh4 {\n\toverflow: hidden;\n\tdisplay: -webkit-box;\n\t-webkit-line-clamp: 3;\n\t-webkit-box-orient: vertical;\n\tline-height: 30px;\n\tfont-size: 30px;\n\tmargin: 0px 0px 0px 0px;\n}\n\np {\n\tcolor: grey;\n\t#line-height: 5px;\n\tfont-size: 1.9em;\n\tmargin: 0 0 0 0;\n}\n\na {\n\ttext-decoration: none;\n\tcolor: black;\n}\n\n.container {\n\tposition: relative;\n\ttext-align: center;\n\tcolor: white;\n}\n\n/* Bottom right text */\n.bottom-right {\n\tposition: absolute;\n\tbackground-color: rgba(25, 25, 25, 0.5);\n\tpadding: 5 5 5 5;\n\tmargin-right: 5;\n\tbottom: 0%;\n\tright: 0%;\n}\n')

def write_log(arg, path, passe):
	var = ''
	for i in arg:
		var += i + ' '
	open(path + 'log', 'a', encoding='utf8').write(time.strftime("%H%M") + '\t' + str(time.time() - passe)[:4] + '\t' + var + '\n')

