from os.path import exists
from .sock import download_xml
from .tools import type_id
from ..analyzer.imports import return_Analyzer

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
		channel = i.split('title="')[1].split('"')[0]
		id_chnl = i.split('xmlUrl="')[1].split('"')[0].replace('https://www.youtube.com/feeds/videos.xml?channel_id=', '')
		if not id_chnl+'\t'+channel in data_sub['[youtube]']:
			data_sub['[youtube]'].append(id_chnl + '\t' + channel)
	write_list(data_sub, path)

def write_list(list_subs, path):
	open(path + 'sub.swy', 'w', encoding='utf8').write('[v][2.0]\n')
	file = open(path + 'sub.swy', 'a', encoding='utf8')
	for site in list_subs:
		file.write('[site]' + site + '\n')
		for i in list_subs[site]:
			file.write(i + '\n')

def add_sub(subs, path=''):
	"""Add a list of subs in sub.swy"""
	list_subs = swy(path, 2)
	for site in subs:
		analyzer = return_Analyzer(site)()
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
	data = open(sub_file, 'rb').read().decode('utf8')
	open(sub_file, 'w', encoding='utf8').write('[v][2.0]\n[site][youtube]\n' + data)

def swy(path, mode=0):
	"""Return a list of sub wich are in sub.swy
	mode : 0 --> return a list with only the id
		   1 --> return a dict with the channel and the id
		   2 --> return a list wich is not .split('\t')"""
	if not exists(path + 'sub.swy'):
		exit("[!] You don't have add you sub")
	urls = dict()
	data_sub = open(path + 'sub.swy', 'rb').read().decode("utf8").split('[site]')
	if not '[v][' in data_sub[0]:
		convert_v1_to_v2(path + 'sub.swy')
	del data_sub[0]
	if mode == 0 or mode == 2:
		for i in data_sub:
			subs = i.split('\n')
			urls[subs[0]] = []
			for y in range(1, len(subs)):
				if subs[y] == '':
					continue
				if mode == 0:
					urls[subs[0]].append(subs[y].split('\t')[0])
				else:
					urls[subs[0]].append(subs[y])
	elif mode == 1:
		for i in data_sub:
			subs = i.split('\n')
			urls[subs[0]] = dict()
			for y in range(1, len(subs)):
				if subs[y] == '':
					continue
				urls[subs[0]][subs[y].split('\t')[0]] = subs[y].split('\t')[1]
	return urls
