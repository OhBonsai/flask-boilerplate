import datetime
TESTING = True

SECRET_KEY = b'\x12\x23'

SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_ECHO = True


REMEMBER_COOKIE_DURATION = datetime.timedelta(7)

