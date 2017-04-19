# This file contains global settings of data_collector
# Created Apr. 19, 2017 by Frederic
GLOBAL_xq = ""
GLOBAL_xnxq01id = "2016-2017-2"
COOKIE_JW = 'JSESSIONID=CC208C85FAC8BC32666123A51452DF8D; BIGipServerpool_jwctest=2068301258.20480.0000'
DEBUG = False

mysql_config = {
    'user': 'everyclass_user',
    'password': 'everyclass_pwd',
    'host': '127.0.0.1',
    'port': '3306',
    'database': 'everyclass',
    'raise_on_warnings': True,
}


def get_semester_code(xq):
    if xq == '':
        return '16_17_2'
    elif xq == '2016-2017-1':
        return '16_17_1'
