# This file contains global settings of data_collector
# Created Apr. 19, 2017 by Frederic
GLOBAL_semester = "2016-2017-2"
DEBUG = True

# MySQL Config
MYSQL_CONFIG = {
    'user': 'everyclass_user',
    'password': 'everyclass_pwd',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'everyclass',
    'raise_on_warnings': True,
}

# Network settings
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8'
COOKIE_JW = 'JSESSIONID=CC208C85FAC8BC32666123A51452DF8D; BIGipServerpool_jwctest=2068301258.20480.0000'
COOKIE_ENG = 'ASPSESSIONIDCAQTSACT=LHBFPBODGNPMGHEPJNLDBNLM; ASP.NET_SessionId=xpud3z45w1hh5i45j4ptf5vd; ASPSESSIONIDCATQSBCT=CDPNOMLDGEHKJGDHDLMJJNEC'
ENGLISH_CLASS_URL = 'http://122.207.65.163/agent161/remote/get_englishClass_2017.asp'
ENGLISH_CLASS_NAMEROLL_URL = 'http://122.207.65.163/agent161/remote/get_englishClass_nameroll_2017.asp'