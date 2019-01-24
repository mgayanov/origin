import requests
import re
import urllib
import urllib2
from random import randint

def dictprinter(d):
	for key in d:
		print("{0}: {1}".format(key, d[key]))

def random_string(length):
	alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz"
	return "".join([alphabet[randint(0,len(alphabet)-1)] for i in range(length)])

class Origin():

	auth_url = "https://signin.ea.com/p/originX/login?execution=e239813213s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fresponse_type%3Dcode%26client_id%3DORIGIN_SPA_ID%26display%3DoriginXWeb%252Flogin%26locale%3Dru_RU%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.origin.com%252Fviews%252Flogin.html"

	user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

	def __init__(self):
		pass

	def GET(self, url, params=None, headers=None):

		response = requests.get(url, params=params, headers=headers)

		response_code = response.status_code
		response_headers = response.headers
		response_html = response.text

		return response_code, response_html, response_headers

	def POST(self, url, params, headers):
		pass

	def auth(self, login, password):



		url = "https://accounts.ea.com/connect/auth"

		values = {
			"response_type": "code",
			"client_id": "ORIGIN_SPA_ID",
			"display": "originXWeb/login",
			"locale": "ru_RU",
			"release_type": "prod",
			"redirect_uri": "https://www.origin.com/views/login.html"
		}

		headers = {
			"User-Agent": '''Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36''',
			"Host": "accounts.ea.com",
			"Connection": "keep-alive",
			"Upgrade-Insecure-Requests": "1",
			"Accept": '''text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8''',
			"Referer": "https://www.origin.com/rus/ru-ru/store/battlefield/battlefield-v",
			"Accept-Encoding": "gzip, deflate, br",
			"Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7"
			#"Cookie": ": _ga=GA1.2.1360172584.1548314489; _gid=GA1.2.1700274289.1548314489; _nx_mpcid=dbbf8fa0-1d6b-4646-8b74-6a302eb11475; utag_main=v_id:01687fa6c81f007ffeb1c4333f4403071014206900bd0$_sn:2$_ss:0$_st:1548335847090$ses_id:1548333559270%3Bexp-session$_pn:3%3Bexp-session"
		}

		#data = urllib.urlencode(values)

		#req = urllib2.Request(url, data)#, headers)

		#response = urllib2.urlopen(req)

		#print (response.info())
		import zlib

		url = "https://accounts.ea.com/connect/auth?response_type=code&client_id=ORIGIN_SPA_ID&display=originXWeb/login&locale=ru_RU&release_type=prod&redirect_uri=https://www.origin.com/views/login.html"
		response_code, response_html, response_headers = self.GET(url, headers=headers)

		#response_code, response_html, response_headers = self.GET(url, headers=headers)
		#decompressed_data = zlib.decompress(response_html, 16 + zlib.MAX_WBITS)

		#print("response_code: {0} response_html: {1}".format(response_code, response_html.encode("utf-8")))

		dictprinter(response_headers)

		fid = re.search('''(?<=login\?fid=)\S+?(?=&)''', response_html)

		print fid.group(0)

		'''
		code, html, headers = self.GET(self.auth_url)

		dictprinter(headers)

		cid = random_string(32)

		form_data = {
			"email": login,
			"password": password,
			"_eventId": "submit",
			"cid": cid,
			"showAgeUp": "true",
			"googleCaptchaResponse": "",
			"_rememberMe": "on"
		}
		'''

origin = Origin()

login = "nick_crichton@hotmail.com"
password = '''Defence123'''

origin.auth(login, password)