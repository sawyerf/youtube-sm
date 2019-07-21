import re
import sys
from os.path import exists
from os import makedirs

from ..downloader.youtube import download_xml
from ..analyzer.imports import return_Analyzer
from .tools import (
	type_id,
	print_debug)

def generate_swy(sub_file, path=''):
	"""Add sub in sub.swy"""
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
	try:
		var = data_sub['[youtube]']
	except:
		data_sub['[youtube]'] = []
	for i in liste:
		channel = re.findall(r'title="(.+?)"', i)[0]
		id_chnl = re.findall(r'channel_id=(.+?)"', i)[0]
		if not id_chnl+'\t'+channel in data_sub['[youtube]']:
			data_sub['[youtube]'].append(id_chnl + '\t' + channel)
	write_list(data_sub, path)

def write_list(list_subs, path):
	open(path + 'sub.swy', 'w', encoding='utf8').write('[v][2.0]\n')
	file = open(path + 'sub.swy', 'a', encoding='utf8')
	for site in list_subs:
		file.write('[site]' + site + '\n')
		for i in list_subs[site]:
			if i != None:
				file.write(i + '\n')

def add_sub(subs, path=''):
	"""Add a list of subs in sub.swy"""
	list_subs = swy(path, 2)
	for site in subs:
		analyzer = return_Analyzer(site)
		if analyzer == None:
			print('[!] The site {} is not support'.format(site))
			continue
		analyzer = analyzer()
		if analyzer == None:
			print('[!] The site {} is not support'.format(site))
			continue
		for sub in subs[site]:
			data = analyzer.add_sub(sub)
			if data != None:
				try:
					list_subs[site].append(data)
				except KeyError:
					list_subs[site] = [data]
	write_list(list_subs, path)

def convert_v1_to_v2(sub_file):
	"""The sub.swy have evolve and is no more compatible so
	this function convert the sub.swy version 1.0 to 2.0"""
	print_debug('[*] Convert swy (v1 to v2)')
	data = open(sub_file, 'rb').read().decode('utf8')
	open(sub_file, 'w', encoding='utf8').write('[v][2.0]\n[site][youtube]\n' + data)

def swy(path, mode=0):
	"""Return a list of sub wich are in sub.swy
	mode : 0 --> return a list with only the id
		   1 --> return a dict with the channel and the id
		   2 --> return a list wich is not .split('\t')"""
	print_debug('[*] Start read swy')
	if not exists(path + 'sub.swy'):
		try:
			open(path + 'sub.swy', 'w', encoding='utf8')
		except:
			print('[!] You didn\'t initialize')
	urls = dict()
	data_sub = open(path + 'sub.swy', 'rb').read().decode("utf8").split('[site]')
	if not '[v][' in data_sub[0]:
		convert_v1_to_v2(path + 'sub.swy')
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
		print_debug("[*] {} subs for {}".format(len(urls[site]), site))
	return urls

def init_swy(path, arg):
	from shutil import rmtree
	if exists(path):
		rmtree(path)
	try:
		makedirs(path + 'data/')
	except:
		exit('[*] Error We Can\'t Create The Folder')
	else:
		print('[*] Data File Create')
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
						print('[!] No tabs in line ' + str(nb_line))
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
			exit('[!] File Not Found (subscription_manager)')
	print('[*] Subs append to sub.swy')
	print('[*] Done')
	exit(0)

