To add a new site you just need to append a class in the folder analyzer and to return your class in the function return_Analyzer(site). For more informations follow this few steps :

1. Fork the Project

2. Clone the project: 
```
git clone https://github.com/[name]/youtube-sm.git 
```
3. Create a new branch : 
```
git checkout -b name_of_the_platform
```
4. Add the class :

    *(All the function are required but if you can't or don't want write some function, define the function with the parameters and pass or return None)*
    ``` python
    from .analyzer	import Analyzer
    
    class Platform_Analyzer(Analyzer):
    	SITE='[platform]'
    	URL_MATCH=r'(?:https://|)(?:www\.|)site\.com/(?P<ID>.*)'
    	def __init__(self, url_id='', min_date=0, mode='', method='0', file=None, prog=None):
    		###################### 
    		# The basic variable #
    		######################
    		self.id = url_id
    		self.mode = mode 
    		self.method = method 
    		self.min_date = min_date
    		###############################
    		# Init the video informations #
    		###############################
    		self.url = ""
    		self.url_channel = "" 
    		self.title = ""
    		self.channel = ""
    		self.date = ""
    		self.data_file = "" 
    		################
    		# The function #
    		################
    		self.prog = prog
    		self.file = file
    
    	def add_sub(self, sub):
    		""" This function return the informations wich are write in sub.swy ."""
    		return id + '\t' + name_of_the_channel_or_playlist
    
    	def real_analyzer(self):
    		""" The main function  wich retrieve the informations and and write it
    		in a file"""
    
    	def old(self, url, lcl):
    		""" The function wich is call with the option -o 
    		This function print the old channel or the dead channel."""
    
    	def dead(self, url):
    		""" The function wich is call with the option -d 
    		This function print the dead channel."""
    ```

5. Return you class in the function return_Analyzer() :
    ```python
    from .youtube import Youtube_Analyzer
    from .platform import Platform_Analyzer # Import your class
    
	analyzer = [
		Youtube_Analyzer,
		Platform_Analyzer, # Add Class
	]
    ```
6. Add, commit and push:
```
git add youtube_sm/analyzer/platform.py
git add youtube_sm/analyzer/imports.py
git commit -m "Add: [platform]"
git push origin platform
```

7. And that's it. You can create a Pull Request and suggest your upgrade.
