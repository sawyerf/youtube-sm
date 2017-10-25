from urllib.request import *


def generate_swy(sub_file):
	data = open(sub_file, 'r').read()
	liste = data.split('<outline')
	del liste[:2]
	for i in liste:
		channel = i.split('title="')[1].split('"')[0]
		id_chnl = i.split('xmlUrl="')[1].split('"')[0].replace('https://www.youtube.com/feeds/videos.xml?channel_id=', '')
		open('sub.swy', 'a').write('{}\t{}\n'.format(id_chnl, channel))

def add_sub(subs):
	for i in subs:
		if i[:2] == 'UC':
			data = urlopen('https://www.youtube.com/feeds/videos.xml?channel_id=' + i).read().decode().split('<name>')[1].split('</name>')[0]
		elif i[:2] == 'PL':
			data = urlopen('https://www.youtube.com/feeds/videos.xml?playlist_id=' + i).read().decode().split('<title>')[1].split('</title>')[0]
		open('sub.swy', 'a').write(i + '\t' +  data + '\n')

