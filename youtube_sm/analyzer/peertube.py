import re
import socket

from datetime     import datetime
from .analyzer    import Analyzer
from ..core.tools import log
from ..downloader.peertube import download_xml_peertube


class Peertube_Analyzer(Analyzer):
	SITE='[peertube]'
	INSTANCES=r'peertube\.mastodon\.host|91video\.online|fightforinfo\.com|video\.lewd\.host|alttube\.fr|aperi\.tube|armstube\.com|artitube\.artifaille\.fr|atchao\.info|banneddata\.me|betamax\.video|bittube\.video|cattube\.org|cinema\.yunohost\.support|conf\.tube|csictv\.csic\.es|devtube\.dev-wiki\.de|dialup\.express|diode\.zone|diytelevision\.com|doby\.io|dreiecksnebel\.alex-detsch\.de|elo-country\.patault\.ovh|evertron\.tv|exode\.me|fanvid\.stopthatimp\.net|fightforinfo\.com|flix\.librenet\.co\.za|fontube\.fr|framatube\.org|freespeech\.tube|gouttedeau\.space|greatview\.video|highvoltage\.tv|hitchtube\.fr|hostyour\.tv|indymotion\.fr|infotik\.fr|irrsinn\.video|juggling\.digital|lepetitmayennais\.fr\.nf|lexx\.impa\.me|libre\.tube|libre\.video|libretube\.net|lostpod\.space|luxtube\.lu|manicphase\.me|marudpeertube\.damnserver\.com|media\.assassinate-you\.net|media\.krashboyz\.org|media\.privacyinternational\.org|media\.zat\.im|medias\.libox\.fr|medias\.pingbase\.net|megatube\.lilomoino\.fr|merci-la-police\.fr|monplaisirtube\.ddns\.net|mplayer\.demouliere\.eu|mytape\.org|mytube\.madzel\.de|nuage\.acostey\.fr|open\.tube|p\.eertu\.be|p0\.pm|peer\.hostux\.social|peer\.mathdacloud\.ovh|peer\.philoxweb\.be|peer\.tube|peertube\.020\.pl|peertube\.1312\.media|peertube\.alcalyn\.app|peertube\.alpharius\.io|peertube\.alter-nativ-voll\.de|peertube\.amicale\.net|peertube\.anarchmusicall\.net|peertube\.anduin\.net|peertube\.anon-kenkai\.com|peertube\.anzui\.de|peertube\.artica\.center|peertube\.askan\.info|peertube\.asrun\.eu|peertube\.at|peertube\.bierzilla\.fr|peertube\.bilange\.ca|peertube\.bittube\.tv|peertube\.ch|peertube\.chantierlibre\.org|peertube\.cipherbliss\.com|peertube\.club|peertube\.co\.uk|peertube\.cojo\.uno|peertube\.cpy\.re|peertube\.cyber-tribal\.com|peertube\.datagueule\.tv|peertube\.david\.durieux\.family|peertube\.ddns\.net|peertube\.debian\.social|peertube\.demonix\.fr|peertube\.desmu\.fr|peertube\.devosi\.org|peertube\.dk|peertube\.donnadieu\.fr|peertube\.dsmouse\.net|peertube\.dynlinux\.io|peertube\.education-forum\.com|peertube\.eric\.ovh|peertube\.esadhar\.net|peertube\.euskarabildua\.eus|peertube\.f-si\.org|peertube\.fedi\.quebec|peertube\.fedilab\.app|peertube\.ffs2play\.fr|peertube\.floss-marketing-school\.com|peertube\.fr|peertube\.freeforge\.eu|peertube\.gaialabs\.ch|peertube\.gcaillaut\.fr|peertube\.gcfamily\.fr|peertube\.gegeweb\.eu|peertube\.gwendalavir\.eu|peertube\.hatthieves\.es|peertube\.heberge\.fr|peertube\.heraut\.eu|peertube\.hugolecourt\.fr|peertube\.iriseden\.eu|peertube\.iselfhost\.com|peertube\.jackbot\.fr|peertube\.kangoulya\.org|peertube\.koehn\.com|peertube\.kosebamse\.com|peertube\.la-famille-muller\.fr|peertube\.laas\.fr|peertube\.lagob\.fr|peertube\.librelabucm\.org|peertube\.linuxrocks\.online|peertube\.live|peertube\.livingutopia\.org|peertube\.lol|peertube\.love|peertube\.mablr\.org|peertube\.makotoworkshop\.org|peertube\.mckillop\.org|peertube\.me|peertube\.montecsys\.fr|peertube\.musicstudio\.pro|peertube\.mxinfo\.fr|peertube\.mygaia\.org|peertube\.nayya\.org|peertube\.nexon\.su|peertube\.nocturlab\.fr|peertube\.nomagic\.uk|peertube\.normandie-libre\.fr|peertube\.opencloud\.lu|peertube\.openstreetmap\.fr|peertube\.opentunisia\.org|peertube\.parleur\.net|peertube\.pcservice46\.fr|peertube\.pl|peertube\.pontostroy\.gq|peertube\.qtg\.fr|peertube\.quaylessed\.icu|peertube\.rainbowswingers\.net|peertube\.roflcopter\.fr|peertube\.schaeferit\.de|peertube\.servebeer\.com|peertube\.serveur\.slv-valbonne\.fr|peertube\.simounet\.net|peertube\.sl-network\.fr|peertube\.slat\.org|peertube\.snargol\.com|peertube\.social\.my-wan\.de|peertube\.solidev\.net|peertube\.stemy\.me|peertube\.storais\.org|peertube\.su|peertube\.swarm\.solvingmaz\.es|peertube\.tamanoir\.foucry\.net|peertube\.tech|peertube\.terranout\.mine\.nu|peertube\.the-penguin\.de|peertube\.ti-fr\.com|peertube\.togart\.de|peertube\.touhoppai\.moe|peertube\.tronic-studio\.com|peertube\.umeahackerspace\.se|peertube\.underworld\.fr|peertube\.uno|peertube\.ventresmous\.fr|peertube\.video|peertube\.volaras\.net|peertube\.we-keys\.fr|peertube\.xoddark\.com|peertube\.xtenz\.xyz|peertube\.zapashcanon\.fr|peertube\.zergy\.net|peertube2\.020\.pl|peertube2\.cpy\.re|peertube3\.cpy\.re|peervideo\.club|peervideo\.ru|peerwatch\.xyz|pire\.artisanlogiciel\.net|pony\.tube|porntube\.ddns\.net|ppstube\.portageps\.org|pt\.forty-two\.nl|pt\.kircheneuenburg\.de|pt\.laurentkruger\.fr|pt\.neko\.bar|pt\.pube\.tk|ptube\.horsentiers\.fr|ptube\.rousset\.nom\.fr|pytu\.be|raptube\.antipub\.org|refuznik\.video|replay\.jres\.org|repro\.video|runtube\.re|scitech\.video|share\.tube|skeptikon\.fr|srv1\.gerifilmai\.ynh\.fr|stage\.peertube\.ch|superduper\.space|thickrips\.cloud|thinkerview\.video|toobnix\.org|troll\.tv|tube\.22decembre\.eu|tube\.4aem\.com|tube\.ac-amiens\.fr|tube\.ac-lyon\.fr|tube\.anjara\.eu|tube\.aps\.systems|tube\.azbyka\.ru|tube\.backbord\.net|tube\.benzo\.online|tube\.blob\.cat|tube\.bn4t\.me|tube\.bootlicker\.party|tube\.bruniau\.net|tube\.calculate\.social|tube\.conferences-gesticulees\.net|tube\.crapaud-fou\.org|tube\.danq\.me|tube\.delalande\.me|tube\.dragonpsi\.xyz|tube\.egf\.mn|tube\.extinctionrebellion\.fr|tube\.fab-l3\.org|tube\.fabrigli\.fr|tube\.fdn\.fr|tube\.fede\.re|tube\.govital\.net|tube\.grin\.hu|tube\.h3z\.jp|tube\.hoga\.fr|tube\.homecomputing\.fr|tube\.interhacker\.space|tube\.kagouille\.fr|tube\.kapussinettes\.ovh|tube\.kdy\.ch|tube\.kher\.nl|tube\.kicou\.info|tube\.ksl-bmx\.de|tube\.lain\.church|tube\.lesamarien\.fr|tube\.linc\.systems|tube\.lou\.lt|tube\.maiti\.info|tube\.maliweb\.at|tube\.midov\.pl|tube\.minzord\.eu\.org|tube\.misterbanal\.net|tube\.mochi\.academy|tube\.nah\.re|tube\.nemsia\.org|tube\.netzspielplatz\.de|tube\.nox-rhea\.org|tube\.nuagelibre\.fr|tube\.nx-pod\.de|tube\.nx12\.net|tube\.odat\.xyz|tube\.openalgeria\.org|tube\.otter\.sh|tube\.ouahpiti\.info|tube\.p2p\.legal|tube\.pasa\.tf|tube\.piweb\.be|tube\.plaf\.fr|tube\.plus200\.com|tube\.postblue\.info|tube\.rebellion\.global|tube\.rfc1149\.net|tube\.rita\.moe|tube\.svnet\.fr|tube\.taker\.fr|tube\.tappret\.fr|tube\.tchncs\.de|tube\.tesgo\.fr|tube\.thechangebook\.org|tube\.traydent\.info|tube\.troopers\.agency|tube\.undernet\.uy|tube\.valinor\.fr|tube\.worldofhauru\.xyz|tube\.yukimochi\.jp|tv\.datamol\.org|tv\.derdorifer\.org|tv\.lapesto\.fr|tv\.mooh\.fr|us\.tv|v\.kretschmann\.social|v\.lastorder\.xyz|v\.lesterpig\.com|v\.mbius\.io|vault\.mle\.party|vid\.lelux\.fi|vid\.lubar\.me|vid\.ncrypt\.at|vid\.y-y\.li|vidcommons\.org|video\.1000i100\.fr|video\.amic37\.fr|video\.anormallostpod\.ovh|video\.antirep\.net|video\.antopie\.org|video\.autizmo\.xyz|video\.blender\.org|video\.blueline\.mg|video\.bruitbruit\.com|video\.cabane-libre\.org|video\.colibris-outilslibres\.org|video\.connor\.money|video\.conquerworld\.fr|video\.coop\.tools|video\.deadsuperhero\.com|video\.devinberg\.com|video\.die-partei\.social|video\.emergeheart\.info|video\.farci\.org|video\.fdlibre\.eu|video\.fediverso\.net|video\.fitchfamily\.org|video\.g3l\.org|video\.gcfam\.net|video\.glassbeadcollective\.org|video\.greenmycity\.eu|video\.gresille\.org|video\.hackers\.town|video\.hardlimit\.com|video\.hdys\.band|video\.ihatebeinga\.live|video\.imagotv\.fr|video\.iphodase\.fr|video\.irem\.univ-paris-diderot\.fr|video\.isurf\.ca|video\.lacaveatonton\.ovh|video\.latavernedejohnjohn\.fr|video\.lemediatv\.fr|video\.lequerrec\.eu|video\.lewd\.host|video\.liberta\.vip|video\.linc\.systems|video\.livecchi\.cloud|video\.lono\.space|video\.lqdn\.fr|video\.lw1\.at|video\.mantlepro\.com|video\.marcorennmaus\.de|video\.migennes\.net|video\.monarch-pass\.net|video\.monsieurbidouille\.fr|video\.nesven\.eu|video\.netsyms\.com|video\.oh14\.de|video\.okaris\.de|video\.omniatv\.com|video\.passageenseine\.fr|video\.ploud\.fr|video\.ploud\.jp|video\.qoto\.org|video\.rastapuls\.com|video\.selea\.se|video\.sftblw\.moe|video\.splat\.soy|video\.subak\.ovh|video\.taboulisme\.com|video\.tedomum\.net|video\.turbo\.chat|video\.typica\.us|video\.valme\.io|video\.vny\.fr|video\.wivodaim\.net|video\.writeas\.org|video\.yukari\.moe|videomensoif\.ynh\.fr|videonaute\.fr|videos-libr\.es|videos\.adhocmusic\.com|videos\.alolise\.org|videos\.benpro\.fr|videos\.cemea\.org|videos\.cloudfrancois\.fr|videos\.coletivos\.org|videos\.dinofly\.com|videos\.domainepublic\.net|videos\.ensilib\.re|videos\.festivalparminous\.org|videos\.funkwhale\.audio|videos\.gerdemann\.me|videos\.globenet\.org|videos\.govanify\.com|videos\.hack2g2\.fr|videos\.hauspie\.fr|videos\.iut-orsay\.fr|videos\.koumoul\.com|videos\.koweb\.fr|videos\.lavoixdessansvoix\.org|videos\.lescommuns\.org|videos\.numerique-en-commun\.fr|videos\.pair2jeux\.tube|videos\.pofilo\.fr|videos\.pueseso\.club|videos\.side-ways\.net|videos\.squat\.net|videos\.tcit\.fr|videos\.ubuntu-paris\.org|videos\.uni-corn\.me|videos\.upr\.fr|videos\.wakapo\.com|videotape\.me|vidz\.dou\.bet|viid\.ga|vis\.ion\.ovh|vloggers\.social|vod\.ksite\.de|vod\.mochi\.academy|watch\.44con\.com|watch\.snoot\.tube|wetube\.ojamajo\.moe|widemus\.de|www\.videos-libr\.es|www\.yiny\.org|xxxporn\.co\.uk|yt\.is\.nota\.live|yunopeertube\.myddns\.me'
	#'
	URL_MATCH=r'(?:http[s]?://|)(?P<Host>%s)/feeds/videos\.xml\?(?:accountId|videoChannelId)=(?P<ID>[0-9]*)' % INSTANCES
	TEST=[
		'https://thinkerview.video/feeds/videos.xml?accountId=5',
		'thinkerview.video:2',
		'peertube.mastodon.host:37295',
	]

	def __init__(self, url_id=''):
		self.id      = self.extract_sub(url_id)

	def extract_sub(self, url):
		match = self.match(url)
		if match:
			return '{}:{}'.format(match.group('Host'), match.group('ID'))
		return url

	def add_sub(self, url):
		""" This function return the informations wich are write in sub.swy ."""
		sub = self.extract_sub(url)
		try:
			data = download_xml_peertube(sub)
		except socket.gaierror:
			log.Error("Wrong host ({})".format(sub))
			return None
		if data is None or '</rss>' not in data:
			log.Error("This sub can't be add.")
			return None
		title = re.findall(r'<title>(.+?)</title>', data)
		if title != []:
			return sub + '\t' + title[0]
		log.Error("This sub can't be add.")

	def real_analyzer(self):
		linfo = download_xml_peertube(self.id)
		if linfo is None:
			return
		for i in linfo:
			content = self.info(i, {
				'url_uploader': {'default': 'https://' + self.id.split(':')[0]},
				'url':          {'re': r'<link>(.*)</link>'},
				'uploader':     {'re': r'<dc:creator>(.*)</dc:creator>'},
				'title':        {'re': r'<title><!\[CDATA\[(.*)\]\]></title>'},
				'image':        {'re': r'<media:thumbnail url="(.*)"'},
				'date':         {'re': r'<pubDate>(.*)</pubDate>', 'date': '%a, %d %b %Y %H:%M:%S GMT'},
			})
			if content is not None:
				self.file.add(**content)

	def old(self, url, since):
		sub = self.extract_sub(url)
		data = download_xml_peertube(sub)
		if data is None:
			self.subis(sub, self.ISDEAD)
		elif data == []:
			self.subis(sub, self.ISEMPTY)
		else:
			content = self.info(data[0], {
				'name':     {'re': r'<dc:creator>(.*)</dc:creator>'},
				'date':        {'re': r'<pubDate>(.*)</pubDate>', 'date': '%a, %d %b %Y %H:%M:%S GMT'},
			})
			if content is None:
				log.Error(sub, ': Fail to parse item')
				return
			if since > content['date']:
				self.subis(content['name'], content['date'])
			else:
				self.subis(content['name'], self.ISOK)

	def dead(self, url):
		sub = self.extract_sub(url)
		data = download_xml_peertube(sub)
		if data is None:
			self.subis(sub, self.ISDEAD)
		elif data == []:
			self.subis(sub, self.ISEMPTY)
		else:
			content = self.info(data[0], {
				'name':     {'re': r'<dc:creator>(.*)</dc:creator>'},
			})
			self.subis(content['name'], self.ISOK)

