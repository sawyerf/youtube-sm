from setuptools import setup, find_packages

params = dict()
params['entry_points'] = {'console_scripts': ['youtube-sm = youtube_sm.commands:main']}

setup(
	name='youtube_sm',
	version='1.1.1',
	url='https://github.com/sawyerf/Youtube_subscription_manager'
	author='Sawyerf',
	author_email='sawyer.flink@protonmail.ch',
	description='Youtube subscription manager',
	long_description=open('README.md', 'r', encoding='utf8').read().replace('\r', ''),
	long_description_content_type='text/markdown',
	keywords='youtube subscription api manager html',
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
