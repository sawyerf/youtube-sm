from setuptools import setup, find_packages

params = dict()
params['entry_points'] = {'console_scripts': ['youtube-sm = youtube_sm.main:main']}

def README():
	try:
		return open('README.md', 'r', encoding='utf8').read().replace('\r', '')
	except:
		return 'Youtube_subscription_manager is an alternative to youtube.com to recover your subscriptions without requires an account.'

setup(
	name='youtube_sm',
	version='2.0.3',
	url='https://gitlab.com/sawyerf/Youtube_subscription_manager',
	author='Sawyerf',
	author_email='sawyer.flink@protonmail.ch',
	description='Youtube subscription manager',
	long_description_content_type='text/markdown',
	long_description=README(),
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
