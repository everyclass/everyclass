from config.default import Config


class DevelopmentConfig(Config):
    # App basic config
    DEBUG = True
    SECRET_KEY = 'development key'
    SERVER_NAME = 'localhost:5000'

    # Database config
    MYSQL_CONFIG = {
        'user': 'everyclass_user',
        'password': 'everyclass_pwd',
        'host': '127.0.0.1',
        'port': '3306',
        'database': 'everyclass',
        'raise_on_warnings': True,
    }
