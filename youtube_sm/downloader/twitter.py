from ..core.download import Download
from ..core.sock import *

import re
import json

def download_twitter(name):
	twitter = download_https('twitter.com', '/' + name)
	if twitter.status != '200':
		return
	token = re.findall('gt=([0-9]*)', twitter.body)[0]

	twimg = download_https('abs.twimg.com', '/responsive-web/web/main.22f2dd14.js')
	if twimg.status != '200':
		return None
	bearer = re.findall('s="Web-12",c="(.+?)"', twimg.body)[0]
	csrf = '4232262aca9e44937ce433580f1d8449'
	# token = '1263211448785866753'

	api = Download(True, 'api.twitter.com')

	api.download('/graphql/-xfUfZsnR_zqjFd-IfrN5A/UserByScreenName?variables=%7B%22screen_name%22%3A%22{}%22%2C%22withHighlightedLabel%22%3Atrue%7D'.format(name.lower()),
		headers={
			'content-type': 'application/json',
			'authorization': 'Bearer ' + bearer,
			'x-guest-token': token,
			'x-twitter-client-language': 'fr',
			'x-twitter-active-user': 'yes',
			'x-csrf-token': csrf,
			'origin': 'https://twitter.com',
			'referer': 'https://twitter.com/',
		},
		status='200'
	)
	if api.status != '200':
		return None
	uid = re.findall('"rest_id":"(.+?)"', api.body)[0]
	api.download('/2/timeline/profile/{}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&userId={}&count=20&ext=mediaStats%2ChighlightedLabel%2CcameraMoment'.format(uid, uid),
		headers={
			'authorization': 'Bearer ' + bearer,
			'x-guest-token': token,
			'x-twitter-client-language': 'fr',
			'x-twitter-active-user': 'yes',
			'x-csrf-token': csrf,
			'origin': 'https://twitter.com',
			'referer': 'https://twitter.com/',
		},
		status='200'
	)
	if api.status == '403':
		data = json.loads(api.body)
		log.Error(name, ': ', data['errors'])
	if api.status != '200':
		return None
	return json.loads(api.body)
