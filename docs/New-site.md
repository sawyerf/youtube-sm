To add a new site you just need to append a class in the folder analyzer and to return your class in the function return_Analyzer(site). For more informations follow this few steps :

1. Fork the Project

2. Clone the project:
```
git clone https://github.com/NAME/youtube-sm.git
```
3. Create a new branch :
```
git checkout -b EXAMPLE
```
4. Add the class :

    *(All the function are required but if you can't or don't want write some function, define the function with the parameters and pass or return None)*
    ``` python
    from .analyzer	import Analyzer
    import re

    class Platform_Analyzer(Analyzer):
    	SITE='[example]'
    	URL_MATCH=r'(?:https://|)(?:www\.|)example\.com/(?P<ID>.*)'
    	TEST=[
    		'https://www.example.com/id',
    	]

    	def __init__(self, sub=''):
    		self.id = self.extract_id(sub)

    	def add_sub(self, sub):
    		"""
    		This function return the informations wich are write in sub.swy.
    		"""
    		id = self.extract_id(sub)
    		if id is None:
    			return None
    		return id + '\t' + CHANNEL

    	def real_analyzer(self):
    		"""
    		The main function wich retrieve the informations and and write it
    		in a file
    		"""
    		data = download_platform(self.id)
    		if data is None:
    			return
    		for element in data:
    			content = self.info(element, {
    				'url':          {'re': r'<link>(.+?)</link>'},
    				'title':        {'re': r'<title>(.+?)</title>'},
    				'uploader':     {'default': self.id},
    				'url_uploader': {'default': 'https://www.example.com/' + self.id},
    				'image':        {'re': r'<img>(.+?)</img>', 'default': self.NO_IMG},
    				'view':         {'re': r'<view>(.+?)</view>'},
    				'date':         {'re': r'<updated>(.+?)</updated>', 'date':'%Y-%m-%dT%H:%M:%S'},
    			})
    			if content is not None:
    				self.file.add(**content)

    	def old(self, url, since):
    		"""
    		This function is call with the option --old.
    		This function print the old channel or the dead channel.
    		"""

    	def dead(self, url):
    		"""
    		This function is call with the option --dead.
    		This function print the dead channel.
    		"""
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
