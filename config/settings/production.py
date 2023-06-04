from config.settings.base import * # noqa

DEBUG = False

ALLOWED_HOSTS = ['gastemenos.club']

BASE_LOG = '/home/ubuntu/logs'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': f"{BASE_LOG}/debug.log"
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'django.template': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
    },
}
