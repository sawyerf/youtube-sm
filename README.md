# Youtube_subscription_manager

[![PyPI](http://img.shields.io/pypi/v/youtube-sm.svg)](http://pypi.python.org/pypi/youtube-sm/)

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Type of File](#type-of-file)
- [Cache](#cache)
- [HTML & RSS](#html--rss)
- [Requirements](#requirements)
- [Compatible](#compatible)
- [Screenshots](#screenshots)

## Description
Youtube_subscription_manager is an alternative to youtube.com to recover your subscriptions without requires an account
*(You can also recover the videos of other platform).*

It can gather informations about every video in a playlist, a channel or your subsciption feed and outputs it as a html page, a detailed list or a list of links.

## Installation
1. Clone the project: `git clone https://github.com/sawyerf/Youtube_suscription_manager.git`
2. Open the folder you just cloned : `cd Youtube_subscription_manager`
3. Execute the setup: `sudo python3 setup.py install`
4. Recover your subscription file in youtube and you are ready to go !

## Usage

1. Download your subscriptions configuration from youtube.com ([here](https://www.youtube.com/subscription_manager?action_takeout=1))
2. Once this is done, you may load it by using the following command :

```
youtube-sm --init [file]
```
3. Finally, you can start using the program using the commands shown below :
```
youtube-sm [OPTIONS]
```

## Commands

```
-h                     Print the help text and exit
-n     [file]          Use an other xml file for your subscriptions
-m     [mode]          Choose the type of the output (html, raw, list, view)
-t     [nb of days]    Choose how far in the past do you want the program to look for videos
-d                     Show the dead channels + those who posted no videos
-o     [nb of months]  Show the channels who didn't post videos in [nb of months] + dead channels
-l     [id]            Analyze only one channel or playlist
-r                     Remove the cache
-s     [id/all]        Outputs the stats of the selected channel(s)
-a     [id]            Append a channel or a playlist at the end of sub.
--init [file]          Remove all your subs and the cache and init with your subscription file.
--af   [file]          Append a file with list of channel or a playlist in sub.swy
--ax   [file]          Append a xml file in sub.swy
--html                 Recover yours subs in the common page web (more videos)
--ultra-html           Recover all the videos with the common page and the button 'load more'
--output [file]        Choose the name of the output file
--cat                  View your subscriptions
--css  [mode]          Import the css files (light, dark, switch)
--loading              Prints a progress bar while running
```

## Example

- Basic
```
youtube-sm
```

- Your sub since 1 month
```
youtube-sm -t 30 --html --css --loading
```

- All the videos of a channel
```
youtube-sm -l UC-lHJZR3Gqxm24_Vd_AJ5Yw -t -1 -m list --loading -r --output test.csv
```

## Type of File
- raw :
```
{date}     {video_id}     {channel_id}     {title}     {channel}     {link_pic}
```
- list :
```
https://www.youtube.com/watch?v={video_id}
```
- view :
```
{views}
```

- html :
```
<!--NEXT -->
<div class="video">
	<a class="left" href="https://www.youtube.com/watch?v={video_id}"> <img src="{link_pic}" ></a>
	<a href="https://www.youtube.com/watch?v={video_id}"><h4>{title}</h4> </a>
	<a href="https://www.youtube.com/channel/{channel_id}"> <p>{channel}</p> </a>
	<p>{date}</p>
	<p class="clear"></p>
</div>
```

## Cache
3 files are generated by the program : `sub.swy`, `log` and `data/`.
- `sub.swy` is a list of yours subscriptions.
- `log` contains the script's time of execution.
- `data/` is a folder where the information for every video are stored.

These 3 files are generated in:
- Windows: `C:\Users\<name>\.youtube_sm\`.
- Linux/MacOS:   `/home/<name>/.cache/youtube_sm/.`.

## HTML & RSS
With youtube-sm you can recover your subscriptions using two methods:
- RSS (default): videos are recovered through an XML page.
- HTML (with --html): videos are recovered through an HTML page.


They are two choice because they cannot recover the same informations and don't require the same amount of time. 
So the default method (the RSS method) is more adapted to recover only the newest videos, whereas the HTML method
is more adapted to recover all the videos of a playlist or to recover its last 30 videos of a channel.

|            | *ULTRA-HTML* | *ULTRA-HTML* |    *HTML*   |    *HTML*    |     *RSS*    |
|:----------:|:------------:|:------------:|:-----------:|:------------:|:------------:|
|            | **Channel**  | **Playlist** | **Channel** | **Playlist** |   **Both**   |
|  Execution |**very** slow |**very** slow |     slow    |     slow     |     Fast     |
|   Number   |    **all**   |    **all**   |  30 videos  |  100 videos  |   15 videos  |
|    Date    |     **~**    |       ✖      |     **~**   |       ✖      |       ✔      |
|  Like Rate |       ✖      |       ✖      |      ✖      |       ✖      |       ✔      |
|    Views   |       ✔      |       ✖      |      ✔      |       ✖      |       ✔      |

## Requirements
- Python 3

## Compatible
- Linux
- Windows
- Android (Termux)
- MacOS

## Screenshots
<p><img src="./screenshot/index.jpg" alt="Phone screen" width=405px height=720px></p>
<p><img src="./screenshot/index_pc.jpg" alt="PC screen" width=100% height=auto></p>
