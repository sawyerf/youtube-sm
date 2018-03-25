from setuptools import setup, find_packages
from os import name

params = dict()
#if name == 'nt':
params['entry_points'] = {'console_scripts': ['youtube-sm = youtube_sm.commands:main']}
#else:
#	params['scripts'] = 'bin/youtube-sm'

setup(
	name='youtube_sm',
	version='1.0.1',
	author='Sawyerf',
	author_email='sawyer.flink@protonmail.ch',
	description='Youtube subscription manager',
	long_description='Command-line program to analyze yours subscriptions and yours playlists from youtube.com',
	license='MLP-2.0',
	packages=find_packages(),
	classifiers=[
		'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
		'Environment :: Console',
		'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only'
	],
	**params
)
