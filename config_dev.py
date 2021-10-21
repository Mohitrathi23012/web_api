import datetime
JWT_TOKEN_LOCATION = ['cookies']
JWT_COOKIE_SECURE = False
JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/token/refresh'
JWT_COOKIE_CSRF_PROTECT = False
JWT_SECRET_KEY = 'jwt-supersecret'
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=3)
