import requests
import re
import urllib
import urllib2
import urlparse
import json
from random import randint

HTTP_200 = 200
HTTP_302 = 302

def dictprinter(d):
	for key in d:
		print("{0}: {1}".format(key, d[key]))

def random_string(length):
	alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz"
	return "".join([alphabet[randint(0,len(alphabet)-1)] for i in range(length)])

class Origin():

	fid          = None
	jssessionid  = None
	sid          = None
	code         = None
	AWSELB       = None
	access_token = None

	user_agent  = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"

	def __init__(self, login, password):
		self.login = login
		self.password = password
		self.cid = random_string(32)

	def __GET(self, url, params=None, headers=None):

		headers = headers or {}

		headers["User-Agent"] = self.user_agent

		response = requests.get(url, params=params, headers=headers, allow_redirects=False)

		response_code    = response.status_code
		response_headers = response.headers
		response_html    = response.text

		return response_code, response_html, response_headers

	def __POST(self, url, data=None, headers=None):

		headers = headers or {}

		headers["User-Agent"] = self.user_agent

		response = requests.post(url, data=data, headers=headers)

		response_code    = response.status_code
		response_headers = response.headers
		response_html    = response.text

		return response_code, response_html, response_headers

	def __OPTIONS(self, url, headers=None):

		headers = headers or {}

		headers["User-Agent"] = self.user_agent

		response = requests.options(url, headers=headers)

		response_code = response.status_code
		response_headers = response.headers
		response_html = response.text

		return response_code, response_html, response_headers

	def __get_fid(self):
		url = "https://accounts.ea.com/connect/auth?response_type=code&client_id=ORIGIN_SPA_ID&display=originXWeb/login&locale=ru_RU&release_type=prod&redirect_uri=https://www.origin.com/views/login.html"

		response_code, response_html, response_headers = self.__GET(url)

		if response_code == HTTP_302:
			self.fid = urlparse.parse_qs(response_headers["Location"][response_headers["Location"].index("?")+1:])['fid'][0]
			return response_headers["Location"]
		else:
			pass

	def __get_JS_sessionid(self, location):
		url = location

		response_code, response_html, response_headers = self.__GET(url)

		if response_code == HTTP_302:
			self.jssessionid = re.search('''(?<=JSESSIONID=)[\S]+?(?=;)''', response_headers["Set-Cookie"]).group(0)
			return "{0}{1}".format("https://signin.ea.com", response_headers["Location"])
		else:
			pass

	def __visit_auth_page(self, location):
		url = location

		headers = {
			"Cookie": "{0}={1}".format("JSESSIONID", self.jssessionid)
		}

		response_code, response_html, response_headers = self.__GET(url, headers=headers)

		if response_code == HTTP_302:
			self.jssessionid = re.search('''(?<=JSESSIONID=)[\S]+?(?=;)''', response_headers["Set-Cookie"]).group(0)
			return response_headers["Location"]


	def __post_auth_data(self, location):
		url = location

		headers = {
			"Cookie": "{0}={1}".format("JSESSIONID", self.jssessionid)
		}

		payload = {
			"email": self.login,
			"password": self.password,
			"_eventId": "submit",
			"cid": self.cid,
			"showAgeUp": "true",
			"googleCaptchaResponse": "",
			"_rememberMe": "on"
		}

		response_code, response_html, response_headers = self.__POST(url, data=payload, headers=headers)

		if response_code == HTTP_200:
			location = re.search('''(?<=window\.location = \")\S+(?=\";)''', response_html).group(0)
			return location

	def __get_sid(self, location):
		url = location

		response_code, response_html, response_headers = self.__GET(url)

		if response_code == HTTP_302:
			self.sid = re.search('''(?<=sid=)[\S]+?(?=;)''', response_headers["Set-Cookie"]).group(0)
			self.code = urlparse.parse_qs(response_headers["Location"][response_headers["Location"].index("?") + 1:])['code'][0]
			return response_headers["Location"]
		else:
			pass

	def __get_AWSELB(self, location):
		url = location

		response_code, response_html, response_headers = self.__GET(url)

		if response_code == HTTP_200:
			self.AWSELB = re.search('''(?<=AWSELB=)[\S]+?(?=;)''', response_headers["Set-Cookie"]).group(0)

	def __get_access_token(self):
		url = "https://accounts.ea.com/connect/auth?client_id=ORIGIN_JS_SDK&response_type=token&redirect_uri=nucleus:rest&prompt=none&release_type=prod"

		headers = {
			"Cookie": "{0}={1}".format("sid", self.sid)
		}

		response_code, response_html, response_headers = self.__GET(url, headers=headers)

		response_json = json.loads(response_html)

		print(response_json)

		if response_code == HTTP_200:
			self.access_token = {
				"access_token": response_json["access_token"].encode("utf-8"),
				"token_type": response_json["token_type"].encode("utf-8")
			}
			print "token: {0}".format(self.access_token)

	def auth(self):

		location = self.__get_fid()

		location = self.__get_JS_sessionid(location)

		self.__visit_auth_page(location)

		location = self.__post_auth_data(location)

		location = self.__get_sid(location)

		self.__get_AWSELB(location)

		self.__get_access_token()


	def view_profile(self):
		url = "https://www.origin.com/views/profile.html"

		headers = {
			"AWSELB": "{0}={1}".format("AWSELB", self.AWSELB)
		}

		response_code, response_html, response_headers = self.__GET(url, headers=headers)

		print(response_code)
		print(response_html)
		dictprinter(response_headers)

	def users(self, userid):
		url = "https://api3.origin.com/atom/users?userIds={}".format(userid)

		response_code, response_html, response_headers = self.__OPTIONS(url)

		headers = {
			"AuthToken": self.access_token["access_token"]
		}

		response_code, response_html, response_headers = self.__GET(url, headers=headers)

		print(response_code)
		print(response_html)
		dictprinter(response_headers)




login = "nick_crichton@hotmail.com"
password = '''Defence123'''


origin = Origin(login, password)

origin.auth()

#origin.view_profile()

origin.users("2258446805")