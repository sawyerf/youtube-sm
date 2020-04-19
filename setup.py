from setuptools	import setup, find_packages
from os		import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	README = f.read()

exec(compile(open('youtube_sm/version.py').read(),
             'youtube_sm/version.py', 'exec'))

setup(
	name='youtube_sm',
	version=__version__,
	url='https://github.com/sawyerf/youtube-sm',
	author='Sawyerf',
	author_email='sawyer.flink@protonmail.ch',
	description='Youtube subscription manager',
	long_description_content_type='text/markdown',
	long_description=README,
	keywords='youtube subscription api manager html',
	license='MLP-2.0',
	packages=find_packages(include=[
		'youtube_sm', 'youtube_sm.*',
	]),
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
	entry_points={
		'console_scripts': ['youtube-sm = youtube_sm.main:main']
	}
)
