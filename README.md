# Youtube_subscription_manager

## Description
Youtube_subscription_manager is a program to analyze yours subscriptions (create a html file with the last videos releases, find the dead channel, etc)

## Usage
1. Recover your subscriprion file in youtube
2. Put this file in the directory
3. Run the script:
``` python3 youTube.py ```
4. Three files are generate `sub.html` or `sub_raw`, `sub.swy` and `log`
    - `sub.html` or `sub_raw` is the file with the last videos
    - `sub.swy` is a list of yours subscriptions
    - `log` is a registre with the time taken by the script, the number of videos found and the hour
- If you want to add a channel. Append the channel id and the name in ` sub.swy`
    - like this: ```channel_id  name ```

## Commands
```
-h                  Print the help text and exit
-n [file]           To use an other xml file for yours subscriptions
-m [mode]           The type of file do you want (html, raw, list)
-t [nb of days]     Numbers of days of subscriptions do you want in your file
-d                  Show the dead channels + those who posted no videos
-o [nb of months]   Show the channels who didn't post videos in nb of months + dead
```

## Type of file
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
- raw :
```
{date}     {video_id}     {channel_id}     {title}     {channel}     {pic}
```
- list :
```
https://www.youtube.com/watch?v={video_id}
```

## Requirements
- Python 3

## Screenshots
<p><img src="./screenshot/index.pnj" alt="Phone screen" width=405px height=720px></p>
