import time
import os

from datetime import datetime, timedelta
import json


class Write_file():
	def __init__(self, output=None, path_cache='', mode='html', method='0', since=7, feed='sub'):
		if output is None:
			output = {
				'html': 'sub.html',
				'json': 'sub.json',
				'list': 'sub_list',
				'raw':  'sub_raw',
			}[mode]
		self.file = open(output, 'w')
		self.mode = mode
		self.contents = []
		self.since = since
		self.data_path = None
		if path_cache is not None:
			self.data_path = f'{path_cache}data/{feed}.{method}.json'
			self.open_cache()

	def open_cache(self):
		if os.path.exists(self.data_path):
			with open(self.data_path, 'r') as f:
				self.contents = json.load(f)
				f.close()
			for content in self.contents:
				if content['date'] != '':
					content['date'] = datetime.strptime(content['date'], '%Y-%m-%d %H:%M:%S')

	def add(self, url='', title='', url_uploader='', image='', uploader='', date='', view=''):
		date = date.replace(microsecond=0)
		for content in self.contents:
			if content['url']['content'] == url:
				return
		content = {
			'url': {
				'content': url,
				'image': image,
				'uploader': url_uploader,
			},
			'date': date,
			'title': title,
			'uploader': uploader,
			'views': view,
		}
		self.contents.append(content)

	def write(self):
		router = {
			'html': self.html,
			'raw': self.raw,
			'list': self.list,
			'json': self.json,
		}
		router[self.mode]()
		# self.file.close()
		if self.data_path is not None:
			with open(self.data_path, 'w') as f:
				json.dump(self.contents, f, indent='\t', default=str)
				f.close()

	def RangeContent(self):
		self.contents = sorted(self.contents, key=lambda k: k['date'], reverse=True)
		if self.since == -1:
			return self.contents
		now = datetime.now() + timedelta(days=3)
		since = datetime.now() - timedelta(days=self.since)
		ncontents = []
		for content in self.contents:
			if since < content['date'] and content['date'] < now:
				ncontents.append(content)
		return ncontents

	def html(self):
		self.file.write(
			'<html>\n' + \
			'	<head>\n' + \
			'		<meta charset="utf-8" />\n' + \
			'		<link rel="stylesheet" href="css/sub.css" />\n' + \
			'		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>\n' + \
			'		<title>Abonnements</title>\n' + \
			'	</head>\n' + \
			'	<body>\n' + \
			'		<!-- {} -->\n'.format(time.ctime()) + \
			'		<div class="But"><input value="" id="but" type="submit" onclick="lol()"></div>\n' + \
			'		<div id="first"></div>\n' + \
			'		<script type="text/javascript" src="css/button.js"></script>\n'
		)
		for content in self.RangeContent():
			self.file.write(
				f'		<!--NEXT -->\n' + \
				f'		<div class="video">\n' + \
				f'			<a class="left" href="{content["url"]["content"]}">\n' + \
				f'				<div class="container">\n' + \
				f'					<img src="{content["url"]["image"]}">\n' + \
				f'					<div class="bottom-right"></div>\n' + \
				f'				</div>\n' + \
				f'			</a>\n' + \
				f'			<a href="{content["url"]["content"]}"><h4>{content["title"]}</h4> </a>\n' + \
				f'			<a href="{content["url"]["uploader"]}"> <p>{content["uploader"]}</p> </a>\n' + \
				f'			<p>{content["date"]}</p>\n' + \
				f'			<p class="clear"></p>\n' + \
				f'		</div>\n' + \
				f'		\n'
			)
		self.file.write('</body></html>')

	def json(self):
		"""
		Write json file
		"""
		contents = self.RangeContent()
		json.dump(contents, self.file, indent='\t', default=str)
		return True

	def raw(self):
		"""
		Write raw file
		"""
		for content in self.RangeContent():
			self.file.write('{date}	{url[content]}	{url[uploader]}	{title}	{uploader}	{url[image]}\n'.format(**content))
		return True

	def list(self):
		"""
		Write list file
		"""
		for content in self.RangeContent():
			self.file.write('{url[content]}\n'.format(**content))


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
	open('css/sub.css', 'a').write(':root {\n--Back: #181a1d;\n--DivHover : #1c1e21;\n--Div: #26292e;\n--ColorH4: #dcdddf;\n--ColorP: grey;\n--ColorBut: #e2e5e9;\n--HeightBut: 0px;\n--HeightButMob: 0px }\n.left { float: left; }\n.clear { clear: both; }\n* { font-family: Arial;}\n\nbody {\nmargin: 0 0 0 0;\nbackground-color: var(--Back);}\n\n.But {\nwidth: 100%;\nposition: fixed;}\n\n#but {\n-webkit-appearance: none;\nborder: none;\nbackground-color: var(--ColorBut);\nwidth: 100%;\nheight: var(--HeightBut); }\n\n#first{\nmargin: 0 27% 0 27%;\nheight: var(--HeightBut); }\n\ndiv.video:hover{ \nbackground-color: var(--DivHover); }\n\ndiv.video {\nbackground-color: var(--Div);\nmargin: 5px 27% 5px 27%; }\n\nimg {\nwidth: 280px;\nheight: 157px;\nmargin-right: 5px;\nobject-fit: cover;\n}\n\nh4 {\ncolor: var(--ColorH4);\nline-height: 18px;\nfont-size: 18px;\nmargin: 0px 0px 10px 0px; }\n\np {\ncolor: var(--ColorP);\nmargin: 4px 0px 4px 0px;\n}\n\na{\ntext-decoration: none;\ncolor: black; }\n\n.description {\noverflow: hidden;\ndisplay: -webkit-box;\n-webkit-line-clamp: 3;\n-webkit-box-orient: vertical;\n  white-space: pre;\n}\n.container {\nposition: relative;\ntext-align: center;\ncolor: white;\n}\n\n/* Bottom right text */\n.bottom-right {\nposition: absolute;\nbackground-color: rgba(25, 25, 25, 0.5);\npadding: 5 5 5 5;\nmargin-right: 5;\nbottom: 0%;\nright: 0%;\n}\n')
	open('css/sub_mobile.css', 'w').write('.left { float:left; }\n.clear { clear: both; }\n* { font-family: Arial; }\n\n\n.description {\noverflow: hidden;\ndisplay: -webkit-box;\n-webkit-line-clamp: 1;\n-webkit-box-orient: vertical;\n}\n#But{\nmargin: 0 0 0 0;\nposition: fixed;\nwidth: 100%;\n}\n\n#but {\nheight: var(--HeightButMob);\nmargin: 0 0 0 0;}\n\n#first{\nmargin: 0 0 0 0;\nwidth: 100%;\nheight: var(--HeightButMob);\n}\n\ndiv.video {\nmargin-left: 0%;\nmargin-right: 0%;\nmargin: 10px 10px 10px 10px; }\n\n\nimg {\nwidth: 380px;\nheight: 214px;\nobject-fit: cover;\n}\n\nh4 {\noverflow: hidden;\ndisplay: -webkit-box;\n-webkit-line-clamp: 3;\n-webkit-box-orient: vertical;\nline-height: 30px;\nfont-size: 30px;\nmargin: 0px 0px 0px 0px;\n}\n\np {\ncolor: grey;\n#line-height: 5px;\nfont-size: 1.9em;\nmargin: 0 0 0 0;\n}\n\na {\ntext-decoration: none;\ncolor: black;\n}\n\n.container {\nposition: relative;\ntext-align: center;\ncolor: white;\n}\n\n/* Bottom right text */\n.bottom-right {\nposition: absolute;\nbackground-color: rgba(25, 25, 25, 0.5);\npadding: 5 5 5 5;\nmargin-right: 5;\nbottom: 0%;\nright: 0%;\n}\n')


def write_log(arg, path, passe):
	if path is None:
		return
	var = ''
	for i in arg:
		var += i + ' '
	open(path + 'log', 'a', encoding='utf8').write(time.strftime("%H%M") + '\t' + str(time.time() - passe)[:4] + '\t' + var + '\n')
