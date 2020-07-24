APPLICATION_NAME = 'Management System'
COMPANY_NAME = 'TECH SPIDER'
FAVICON_URL = 'base/custom/img/favicon.ico'
COMPANY_NAME_ICON_URL = 'base/custom/img/__TS_logo_transparent.png'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_EXEMPT_URLS = [
    'admin/',
    'reset/',
    'registration/',
    'api/*',
]
