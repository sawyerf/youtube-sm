# Youtube_subscription_manager

## Description
Youtube_subscription_manager is a program to analyze yours subscriptions (create a html file with the last videos releases, find the dead channel, etc)

## Installation
1. Clone the project: `git clone https://github.com/sawyerf/Youtube_suscription_manager.git`
2. Go in the folder: `cd Youtube_subscription_manager`
3. Execute the setup: `sudo python3 setup.py install` 
4. Recover your subscriprion file in youtube and go !!!

## Usage
```youtube-sm [OPTIONS]```

## Commands

```
-h                  Print the help text and exit
-n  [file]          To use an other xml file for yours subscriptions
-m  [mode]          The type of file do you want (html, raw, list)
-t  [nb of days]    Numbers of days of subscriptions do you want in your file
-d                  Show the dead channels + those who posted no videos
-o  [nb of months]  Show the channels who didn't post videos in nb of months + dead
-a  [id]            To append a channel or a playlist at the end of sub.swy
-af [file]          To append a file with list of channel or a playlist in sub.swy
-ax [file]	    To append a xml file in sub.swy
-l  [id]            If you want to analyze only one channel or playlist
-r		    To remove the cache before analyze
-s  [id/all]        To have the stat of the channel(s)
```

## Type of file
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

## Requirements
- Python 3

## Compatible
- Linux
- Android (Termux)
- Windows
- MacOS (I don't known)

## Screenshots
<p><img src="./screenshot/index.jpg" alt="Phone screen" width=405px height=720px></p>
<p><img src="./screenshot/index_pc.jpg" alt="PC screen" width=720px height=405px></p>
