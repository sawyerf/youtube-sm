from urllib.request import *

def html_process(i):
	url = i.split('<yt:videoId>')[1].split('</yt:videoId>')[0]
	url_channel = i.split('<yt:channelId>')[1].split('</yt:channelId>')[0]
	title = i.split('<media:title>')[1].split('</media:title>')[0]
	date = i.split('<published>')[1].split('T')[0]
	if url in open('data/' + date, 'r').read():
		return
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
		image = image + data.split(image)[1].split('">')[0]
	except:
		print(title, image , url_channel)
	open('data/' + date, 'a').write("""<!--NEXT -->
<div class="video">
<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="{}" ></a>
<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
<p>{}</p>
<p class="clear"></p></div>
<!--NEXT -->
""".format(url, image, url, title, date))



def html_init():
	open('sub.html', 'w').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="style_sub.css" />
		<title>Abonnements</title>
	</head>
	<body>
""")
