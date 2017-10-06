from urllib.request import *
import os 
import time

def html_process(i):
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
			else:
				return
	except:
		try:
			os.mkdir('data/' + date[0])
		except:
			pass
	try:
		data = open('cache/' + url_channel, 'r').read()
	except:
		req = Request('https://www.youtube.com/channel/' + url_channel + '/videos', headers={'User-Agent':'Mozilla/5.0'})
		nb = 0
		while nb != 5:
			try:
				data = urlopen(req).read().decode()
			except:
				nb += 1
			else:
				break
		open('cache/' + url_channel, 'w').write(data)
	
	image = i.split('<media:thumbnail url="')[1].split('"')[0]
	image = 'https://i.y' + image.split('.y')[1]
	try:
		image = image + data.split(image)[1].split('"')[0]
	except:
		image = 'https://i.ytimg.com/vi/PF06Tk4z2bo/hqdefault.jpg?sqp=-oaymwEWCMQBEG5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLBGqMLakE2aELko2V5i7N48o2sECw'
	open('data/' + date[0] + '/' + date[1], 'a').write("""<!--NEXT -->
<div class="video">
<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="{}" ></a>
<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
<a href="https://www.youtube.com/channel/{}"> <p>{}</p> </a>
<p>{}</p>
<p class="clear"></p></div>
""".format(url, image, url, title, url_channel, channel, date[0]))


def html_init():
	try:
		os.mkdir('cache')
	except:
		pass
	try:
		os.mkdir('data')
	except:
		pass
	fch = os.listdir('cache/')
	for i in fch:
		os.remove('cache/' + i)
	open('sub.html', 'w').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="style_sub.css" />
		<title>Abonnements</title>
	</head>
	<body>
<!-- {} -->
""".format(time.ctime()))
