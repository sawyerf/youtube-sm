import re
import sys
from os.path import exists
from os import makedirs
from shutil import rmtree

from ..analyzer.imports import (
	return_Analyzer,
	UrlToAnalyzer,
)
from .tools import (
	log)


def write_list(list_subs, path):
	open(path + 'sub.swy', 'w', encoding='utf8').write('[v][2.0]\n')
	file = open(path + 'sub.swy', 'a', encoding='utf8')
	for site in list_subs:
		file.write('[site]' + site + '\n')
		for i in list_subs[site]:
			if i is not None:
				file.write(i + '\n')


def generate_swy(sub_file, path=''):
	"""
	Add sub in sub.swy
	"""
	if exists(sub_file):
		data = open(sub_file, 'r', encoding="utf8").read()
	else:
		exit('[!] File not found (' + sub_file + ')')
	liste = data.split('<outline')
	del liste[:2]
	if not exists(path + 'sub.swy'):
		open(path + 'sub.swy', 'a', encoding='utf8').write('[v][2.0]\n[site][youtube]\n')
		data_sub = {'[youtube]': []}
	else:
		data_sub = swy(path, 2)
	for i in liste:
		channel = re.findall(r'title="(.+?)"', i)[0]
		id_chnl = re.findall(r'channel_id=(.+?)"', i)[0]
		if id_chnl+'\t'+channel not in data_sub['[youtube]']:
			data_sub['[youtube]'].append(id_chnl + '\t' + channel)
	write_list(data_sub, path)


def add_suburl(url, path=''):
	list_subs = swy(path, 2)
	analyzer = UrlToAnalyzer(url)
	if analyzer is None:
		log.Error('The url {} is not support'.format(url))
		return
	analyzer = analyzer()
	if analyzer is None:
		log.Error('The url {} is not support'.format(url))
		return
	data = analyzer.add_sub(url)
	if data is None:
		log.Error('Failed to add ', url)
	else:
		log.RInfo('Add: ', data)
	if data is not None:
		if analyzer.SITE in list_subs:
			list_subs[analyzer.SITE].append(data)
		else:
			list_subs[analyzer.SITE] = [data]
	write_list(list_subs, path)


def add_sub(subs, path=''):
	"""
	Add a list of subs in sub.swy
	"""
	list_subs = swy(path, 2)
	for site in subs:
		analyzer = return_Analyzer(site)
		if analyzer is None:
			log.Error('The site {} is not support'.format(site))
			continue
		analyzer = analyzer()
		if analyzer is None:
			log.Error('The site {} is not support'.format(site))
			continue
		for sub in subs[site]:
			data = analyzer.add_sub(sub)
			if data is not None:
				if site in list_subs:
					list_subs[site].append(data)
				else:
					list_subs[site] = [data]
	write_list(list_subs, path)


def swy(path, mode=0):
	"""
	Return a list of sub wich are in sub.swy
	mode :	0 --> return a list with only the id
			1 --> return a dict with the channel and the id
			2 --> return a list wich is not .split('\t')
	"""
	log.Info('Start read swy')
	if not exists(path + 'sub.swy'):
		try:
			open(path + 'sub.swy', 'w', encoding='utf8')
		except:
			log.Error('You didn\'t initialize')
	urls = dict()
	data_sub = open(path + 'sub.swy', 'rb').read().decode("utf8").split('[site]')
	del data_sub[0]
	if mode == 0 or mode == 2:
		for i in data_sub:
			subs = i.split('\n')
			siteid = subs[0].rstrip()
			urls[siteid] = []
			for y in range(1, len(subs)):
				if subs[y] == '':
					continue
				if mode == 0:
					urls[siteid].append(subs[y].split('\t')[0])
				else:
					urls[siteid].append(subs[y])
	elif mode == 1:
		for i in data_sub:
			subs = i.split('\n')
			siteid = subs[0].rstrip()
			urls[siteid] = dict()
			for y in range(1, len(subs)):
				if subs[y] == '':
					continue
				urls[siteid][subs[y].split('\t')[0]] = subs[y].split('\t')[1]
	for site in urls:
		log.Info("{} subs for {}".format(len(urls[site]), site))
	return urls


def init_swy(path, arg):
	if exists(path):
		rmtree(path)
	makedirs(path + 'data/')
	log.Info('Data Folder Create')
	if len(sys.argv) != arg + 1:
		add_file = sys.argv[arg + 1]
		if not exists(add_file):
			exit('[!] File Not Found (' + add_file + ')')
		if add_file[len(add_file) - 4:] == '.swy':
			with open(add_file, 'rb') as file, open(path + 'sub.swy', 'a', encoding='utf8') as sub_file:
				nb_line = 1
				while True:
					line = file.readline().decode('utf8')
					if '\t' in line or '[site]' in line or '[v]' in line:
						sub_file.write(line)
					elif line == '':
						break
					else:
						log.Error('No tabs in line ' + str(nb_line))
		elif add_file[len(add_file) - 5:] == '.json':
			subs = dict()
			data = open(add_file, 'rb').read().decode('utf8')
			subs['[youtube]'] = re.findall(r'channel/(.{24})', data)
			add = re.findall(r'youtube.com/playlist\?list=(.{34})', data)
			subs['[youtube]'] = [*subs['[youtube]'], *add]
			add_sub(subs, path)
		else:
			generate_swy(add_file, path=path)
	else:
		if exists('subscription_manager'):
			generate_swy('subscription_manager', path=path)
		else:
			log.Error('File Not Found (subscription_manager)')
			exit()
	log.Info('Done')
	exit(0)
