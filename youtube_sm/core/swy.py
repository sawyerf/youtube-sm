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


def write_list(list_subs, path, feed):
	open(path + feed + '.swy', 'w', encoding='utf8').write('[v][2.0]\n')
	file = open(path + feed + '.swy', 'a', encoding='utf8')
	for site in list_subs:
		file.write('[site]' + site + '\n')
		for i in list_subs[site]:
			if i is not None:
				file.write(i + '\n')


def generate_swy(sub_file, path='', feed='sub'):
	"""
	Add sub in sub.swy
	"""
	if exists(sub_file):
		data = open(sub_file, 'r', encoding="utf8").read()
	else:
		exit('[!] File not found (' + sub_file + ')')
	liste = data.split('<outline')
	del liste[:2]
	if not exists(path + feed + '.swy'):
		open(path + feed + '.swy', 'a', encoding='utf8').write('[v][2.0]\n[site][youtube]\n')
		data_sub = {'[youtube]': []}
	else:
		data_sub = swy(path, 2, feed)
	for i in liste:
		channel = re.findall(r'title="(.+?)"', i)[0]
		id_chnl = re.findall(r'channel_id=(.+?)"', i)[0]
		if id_chnl+'\t'+channel not in data_sub['[youtube]']:
			data_sub['[youtube]'].append(id_chnl + '\t' + channel)
	write_list(data_sub, path, feed)


def add_suburl(url, path='', feed='sub'):
	list_subs = swy(path, 2, feed)
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
	write_list(list_subs, path, feed)


def add_sub(subs, path='', feed='sub'):
	"""
	Add a list of subs in sub.swy
	"""
	list_subs = swy(path, 2, feed)
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
			if data is None:
				log.Error('Failed to add ', sub)
			else:
				log.Info('Add: ', data)
				if site in list_subs:
					list_subs[site].append(data)
				else:
					list_subs[site] = [data]
	write_list(list_subs, path, feed='sub')

def swy(path, mode=0, feed='sub'):
	"""
	Return a list of sub wich are in sub.swy
	mode :	0 --> return a list with only the id
			1 --> return a dict with the channel and the id
			2 --> return a list wich is not .split('\t')
	"""
	log.Info('Start read swy')
	if not exists(path + feed + '.swy'):
		try:
			open(path + feed + '.swy', 'w', encoding='utf8')
		except:
			log.Error('You didn\'t initialize')
	urls = dict()
	data_sub = open(path + feed + '.swy', 'rb').read().decode("utf8").split('[site]')
	del data_sub[0]
	for i in data_sub:
		subs = i.split('\n')
		siteid = subs[0].rstrip()
		if mode == 0 or mode == 2:
			urls[siteid] = []
		elif mode == 1:
			urls[siteid] = dict()
		for y in range(1, len(subs)):
			if subs[y] == '':
				continue
			if mode == 0:
				urls[siteid].append(subs[y].split('\t')[0])
			elif mode == 1:
				urls[siteid][subs[y].split('\t')[0]] = subs[y].split('\t')[1]
			elif mode == 2:
				urls[siteid].append(subs[y])
	for site in urls:
		log.Info("{} subs for {}".format(len(urls[site]), site))
	return urls


def init_swy(path, arg, feed):
	if exists(path):
		rmtree(path)
	makedirs(path + 'data/')
	log.Info('Data Folder Create')
	if len(sys.argv) != arg + 1:
		add_file = sys.argv[arg + 1]
		if not exists(add_file):
			exit('[!] File Not Found (' + add_file + ')')
		if add_file[len(add_file) - 4:] == '.swy':
			with open(add_file, 'rb') as file, open(path + feed + '.swy', 'a', encoding='utf8') as sub_file:
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
			add_sub(subs, path, feed)
		else:
			generate_swy(add_file, path, feed)
	else:
		if exists('subscription_manager'):
			generate_swy('subscription_manager', path, feed)
		else:
			log.Error('File Not Found (subscription_manager)')
			exit()
	log.Info('Done')
	exit(0)
