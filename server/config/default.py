class Config(object):
    # App basic config
    DEBUG = True
    SECRET_KEY = 'development key'
    SERVER_NAME = 'localhost'

    # Database config
    MYSQL_CONFIG = {
                       'user': 'database_user',
                       'password': 'database_password',
                       'host': '127.0.0.1',
                       'port': '6666',
                       'database': 'everyclass',
                       'raise_on_warnings': True,
                   },

    # Business
    SEMESTER = '2016-2017-2'
    DATA_LAST_UPDATE_TIME = 'Apr. 29, 2017'
