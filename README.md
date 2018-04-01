# Youtube_subscription_manager

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Type of File](#type-of-file)
- [Cache](#cache)
- [Requirements](#requirements)
- [Compatible](#compatible)
- [Screenshots](#screenshots)

## Description
Youtube_subscription_manager is a program to analyze yours subscriptions (create a html file with the last videos releases, find the dead channel, etc)

## Installation
1. Clone the project: `git clone https://github.com/sawyerf/Youtube_suscription_manager.git`
2. Go in the folder: `cd Youtube_subscription_manager`
3. Execute the setup: `sudo python3 setup.py install`
4. Recover your subscriprion file in youtube and go !!!

## Usage
1. After have recover your subs file
2. Execute the commands: `youtube-sm --init [file]` ( [file] is optionnal ).
3. You can begin to use:

```
youtube-sm [OPTIONS]
```

## Commands

```
-h                     Print the help text and exit
-n     [file]          To use an other xml file for yours subscriptions
-m     [mode]          The type of file do you want (html, raw, list)
-t     [nb of days]    Numbers of days of subscriptions do you want in your file
-d                     Show the dead channels + those who posted no videos
-o     [nb of months]  Show the channels who didn't post videos in nb of months + dead channels
-l     [id]            If you want to analyze only one channel or playlist
-r                     To remove the cache before analyze
-s     [id/all]        To have the stat of the channel(s)
-a     [id]            To append a channel or a playlist at the end of sub.
--init [file]          Remove all your subs and the cache and init with your subscription file.
--af   [file]          To append a file with list of channel or a playlist in sub.swy
--ax   [file]          To append a xml file in sub.swy
--cat                  To view your subs
--css                  Import the css files
--loading              To print a progress bar
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
3 File are generate in Windows and Linux: `sub.swy`, `log`, `data/`.
- `sub.swy` is a list of yours subscriptions.
- `log` is a registre with the time taken by the script.
- `data/` is a folder which store all the informations of each videos

This 3 files are generate in:
- Windows: `C:\Users\<name>\.youtube_sm\`.
- Linux:   `/home/<name>/.cache/youtube_sm/.`.

## Requirements
- Python 3

## Compatible
- Linux
- Windows
- Android (Termux)
- MacOS (I don't known)

## Screenshots
<p><img src="./screenshot/index.jpg" alt="Phone screen" width=405px height=720px></p>
<p><img src="./screenshot/index_pc.jpg" alt="PC screen" width=100% height=auto></p>
