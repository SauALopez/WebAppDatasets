class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADS = "./app/static/files/uploads"
    REPORTS = "./app/static/files/reports"
    QSTR_DEFAULT = "humidity"
    SENSOR_SQUEMA = ["temperature","humidity","light", "voltage"]
    SESSION_COOKIE_SECURE = True

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    UPLOADS = "./app/static/files/uploads"
    QSTR_DEFAULT = "humidity"

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = False
