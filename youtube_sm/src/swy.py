from os.path import exists
from .sock import download_xml
from .tools import type_id

def generate_swy(sub_file, path=''):
	"""Add sub in sub.swy"""
	if exists(sub_file):
		data = open(sub_file, 'r', encoding="utf8").read()
	else:
		exit('[!] File not found (' + sub_file + ')')
	liste = data.split('<outline')
	del liste[:2]
	open(path + 'sub.swy', 'a', encoding='utf8').write('[v][2.0]\n[site][youtube]')
	for i in liste:
		channel = i.split('title="')[1].split('"')[0]
		id_chnl = i.split('xmlUrl="')[1].split('"')[0].replace('https://www.youtube.com/feeds/videos.xml?channel_id=', '')
		open(path + 'sub.swy', 'a', encoding='utf8').write('{}\t{}\n'.format(id_chnl, channel))

def add_sub(subs, path=''):
	"""Add a list of subs in sub.swy"""
	for i in subs:
		tid = type_id(i)
		data = download_xml(i, type_id=tid, split=False)
		if data == None:
			continue
		try:
			if tid:
				data = data.split('<name>')[1].split('</name>')[0]
			else:
				data = data.split('<title>')[1].split('</title>')[0]
			open(path + 'sub.swy', 'a', encoding='utf8').write(i + '\t' +  data + '\n')
		except:
			pass

def convert_v1_to_v2(sub_file):
	"""The sub.swy have evolve and is no more compatible so 
	this function can convert the sub.swy"""
	data = open(sub_file, 'rb').read().decode('utf8')
	open(sub_file, 'w', encoding='utf8').write('[v][2.0]\n[site][youtube]\n' + data)

def swy(sub_file='subscription_manager', path='', liste=True):
	"""Generate a list of subs which are append in sub.swy and return"""
	if not exists(path + 'sub.swy'):
		generate_swy(sub_file, path)
	urls = dict()
	data_sub = open(path + 'sub.swy', 'rb').read().decode("utf8").split('[site]')
	if not '[v][' in data_sub[0]:
		convert_v1_to_v2(path + 'sub.swy')
	del data_sub[0]
	if liste:
		for i in data_sub:
			subs = i.split('\n')
			urls[subs[0]] = []
			for y in range(1, len(subs)):
				if subs[y] == '':
					continue
				urls[subs[0]].append(subs[y].split('\t')[0])
	else:
		for i in data_sub:
			subs = i.split('\n')
			urls[subs[0]] = dict()
			for y in range(1, len(subs)):
				if subs[y] == '':
					continue
				urls[subs[0]][subs[y].split('\t')[0]] = subs[y].split('\t')[1]
	return urls
