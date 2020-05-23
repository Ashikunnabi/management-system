APPLICATION_NAME = 'Management System'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_EXEMPT_URLS = [
    'admin/',
    'reset/',
    'registration/',
    'api/*',
]
