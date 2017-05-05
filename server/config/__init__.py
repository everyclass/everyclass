import os


def load_config():
    mode = os.environ.get('MODE')
    try:
        if mode == 'PRODUCTION':
            from .production import ProductionConfig
            return ProductionConfig
        else:
            from .development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError as e:
        from .default import Config
        return Config
