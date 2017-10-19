from urllib.request import *
import os 
import time


def xml_recup(url):
	nb = 0
	while True:
		try:
			data = urlopen('https://www.youtube.com/feeds/videos.xml?channel_id=' +  url).read().decode()
		except :
			nb += 1
			if nb == 3:
				return False
		else:
			break
	linfo = data.split("<entry>")
	del linfo[0]
	if linfo == []:
		return None
	return linfo

def html_start(url_data, min_date):
	nb_new = 0
	for url in url_data:
		linfo = xml_recup(url)
		if linfo == False:
			continue
		for i in linfo:
			date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
			if min_date <= date:
				dvid = html_process(i)
				if dvid:
					nb_new += 1
				else:
					break
			else:
				break
	return nb_new

def html_end():
	fch = sorted(os.listdir('data/'))
	for i in range(7):
		fch_in = sorted(os.listdir('data/' + fch[-1-i]))
		for a in range(len(fch_in)):
			data = open('data/' + fch[-1-i] + '/' + fch_in[-1-a], 'r').read()
			open('sub.html', 'a').write(data)
	open('sub.html', 'a').write('</body></html>')

def html_process(i):
	dvid = True
	url = i.split('<yt:videoId>')[1].split('</yt:videoId>')[0]
	url_channel = i.split('<yt:channelId>')[1].split('</yt:channelId>')[0]
	title = i.split('<media:title>')[1].split('</media:title>')[0]
	channel = i.split('<name>')[1].split('</name>')[0]
	date = i.split('<published>')[1].split('+')[0].split('T')
	try:
		data = open('data/' + date[0] + '/' + date[1], 'r+').read()
		if url in data:
			if 'https://i.ytimg.com/vi/PF06Tk4z2bo/hqdefault.jpg?sqp=-oaymwEWCMQBEG5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLBGqMLakE2aELko2V5i7N48o2sECw' in data:
				os.remove('data/' + date[0] + '/' + date[1])
				dvid = False
			else:
				return False
		else:
			pass
	except:
		try:
			os.mkdir('data/' + date[0])
		except:
			pass
	image = 'https://i.ytimg.com/vi/' + url  + '/mqdefault.jpg'
	open('data/' + date[0] + '/' + date[1], 'a').write("""<!--NEXT -->
<div class="video">
	<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="{}" ></a>
	<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
	<a href="https://www.youtube.com/channel/{}"> <p>{}</p> </a>
	<p>{}</p>
	<p class="clear"></p>
</div>
""".format(url, image, url, title, url_channel, channel, date[0]))
	if dvid:
		return True
	else:
		return False

def html_init():
	try:
		os.mkdir('data')
	except:
		pass
	open('sub.html', 'w').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="css/sub.css" />
		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>
		<title>Abonnements</title>
	</head>
	<body>
<!-- {} -->
""".format(time.ctime()))
