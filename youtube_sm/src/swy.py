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

def swy(sub_file='subscription_manager', path='', liste=True):
	"""Generate a list of subs which are append in sub.swy and return"""
	if not exists(path + 'sub.swy'):
		generate_swy(sub_file, path)
	data_sub = open(path + 'sub.swy', 'rb').read().decode("utf8").split('\n')
	if liste:
		url_data = []
		for i in data_sub:
			url_data.append(i.split('\t')[0])
	else:
		url_data = dict()
		for i in data_sub:
			ch = i.split('\t')
			try:
				url_data[ch[0]] = ch[1]
			except:
				pass
	return url_data

