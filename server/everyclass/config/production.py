from config.default import Config


class DevelopmentConfig(Config):
    # App config
    DEBUG = False
    SECRET_KEY = '9*+X{fW^d@62uNHeFXEArkcAh'
    SERVER_NAME = 'every.admirable.one'

    # Database config
    MYSQL_CONFIG = {
                       'user': 'everyclass_user',
                       'password': 'everyclass_pwd',
                       'host': '127.0.0.1',
                       'port': '3306',
                       'database': 'everyclass',
                       'raise_on_warnings': True,
                   },
