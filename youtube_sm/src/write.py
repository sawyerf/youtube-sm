import time
import os

from .time import since

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
			else:
				self.output = 'sub'
		self.mode = mode
		self.method = method
		self.path_cache = path_cache # The path where the data and the sub are stock

	def write(self, url='', title='', url_channel='', channel='', date='', data_file='', view='', type_id=''):
		"""Write the information in a file"""
		if self.mode == 'html':
			return self.generate_data_html(url, title, url_channel, channel, date, data_file)
		elif self.mode == 'raw':
			return self.append_raw(url, title, url_channel, channel, date, data_file, type_id)
		elif self.mode == 'list':
			return self.append_list(url, data_file, type_id)
		elif self.mode == 'view':
			return self.append_view(view)

	def html_init(self):
		"""To init the html file"""
		try:
			os.mkdir(self.path_cache + 'data/' + self.method)
		except:
			pass
		open(self.output, 'w').write('<html>\n	<head>\n		<meta charset="utf-8" />\n		<link rel="stylesheet" href="css/sub.css" />\n		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>\n		<title>Abonnements</title>\n	</head>\n	<body>\n<!-- {} -->'.format(time.ctime()))

	def append_raw(self, url, title, url_channel, channel, date, data_file, type_id):
		"""Append the informations wich are been recover 
		in the file 'sub_raw'."""
		if self.method == '0':
			var = data_file[0] + data_file[1].replace(':', '') + '\t' + date + '\t' + url + '\t' + url_channel + '\t' + title + '\t' + channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(url) + '\n'
			if len(var) > 350:
				return False
			open(self.output, 'a', encoding='utf8').write(var)
		elif self.method == '1' or self.method == '2':
			if type_id == True:
				var = data_file[0] + '000000' + '\t' + url + '\t' + url_channel + '\t' + title + '\t' + channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(url) + '\n'
			else:
				var = '00000000000000' + '\t' + url + '\t' + url_channel + '\t' + title + '\t' + channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(url) + '\n'
			if len(var) > 350:
				return False
			open(self.output, 'a', encoding='utf8').write(var)
		var = ""
		return True

	def append_list(self, url, data_file, type_id):
		""""Append the informations wich are been recover
		in the file 'sub_raw'. The date is add to sort the
		videos, but it's deleted"""
		if len(url) != 11:
			return False
		if self.method == '0':
			open(self.output, 'a', encoding='utf8').write(data_file[0] + data_file[1].replace(':', '') + ' https://www.youtube.com/watch?v=' + url + '\n')
		elif self.method == '1' or self.method == '2':
			if type_id:
				open(self.output, 'a', encoding='utf8').write(data_file[0] + '000000' + ' https://www.youtube.com/watch?v=' + url + '\n')
			else:
				open(self.output, 'a', encoding='utf8').write('00000000000000' + ' https://www.youtube.com/watch?v=' + url + '\n')
		return True

	def append_view(self, view):
		""" Write the views in a file"""
		if view != None:
			open(self.output, 'a', encoding='utf8').write(view + '\n')

	def generate_data_html(self, url, title, url_channel, channel, date, data_file):
		"""Append the informations wich are been recover
		in a file in '.../data/[date]/.' """
		try:
			data = open('{}data/{}/{}/{}'.format(self.path_cache, self.method, data_file[0], data_file[1].replace(':', '')), 'rb+').read().decode("utf8")
			if url in data:
				return False
		except:
			try:
				os.mkdir(self.path_cache + 'data/' + self.method + '/' + data_file[0])
			except:
				pass
		if url_channel[:2] == 'UC':
			url_channel = 'channel/' + url_channel
		elif url_channel[:8] == 'results?':
			pass
		else:
			url_channel = 'user/' + url_channel
		open('{}data/{}/{}/{}'.format(self.path_cache, self.method, data_file[0], data_file[1].replace(':', '')), 'a', encoding='utf-8').write("""<!--NEXT -->
<div class="video">
	<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="https://i.ytimg.com/vi/{}/mqdefault.jpg" ></a>
	<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
	<a href="https://www.youtube.com/{}"> <p>{}</p> </a>
	<p>{}</p>
	<p class="clear"></p>
</div>
""".format(url, url, url, title, url_channel, channel, date))
		return True

	def sort_file(self, count=7):
		""" To sort the videos by date or add the videos in the file"""
		if self.mode == 'html':
			self.html_end(count)
		elif self.mode == 'list' or self.mode == 'raw':
			self.raw_list_end(count)

	def html_end(self, count=7, play=True):
		"""Recover the file in '.../data/.' with all the
		informations, sort by date and add the informations
		in './sub.html'. """
		fch = sorted(os.listdir(self.path_cache + 'data/' + self.method + '/'))
		if len(fch) < count:
			date = 0
		elif count == -1:
			date = -1
		else:
			date = int(since(count)[:8])
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
			if folder_date > date:
				fch_in = sorted(os.listdir(self.path_cache + 'data/' + self.method + '/' + fch[-1-i]))
				for a in range(len(fch_in)):
					data = open(self.path_cache + 'data/' + self.method + '/' + fch[-1-i] + '/' + fch_in[-1-a], 'r', encoding='utf-8').read()
					sub_file.write(data)
		sub_file.close()
		open(self.output, 'a').write('</body></html>')

	def raw_list_end(self, count=7):
		"""Sorted the videos by date"""
		linfo = sorted(open(self.output, 'rb').read().decode('utf8').replace('\r', '').split('\n'))
		fichier = open(self.output, 'w', encoding='utf8')
		if count == -1:
			date = -1
		else:
			date = int(since(count)[:8])
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
