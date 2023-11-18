from .base import *

DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1", "minion", "minion.salnikov.us", "photo-archive.net", "www.photo-archive.net"
]

CSRF_TRUSTED_ORIGINS = ["htps://photo-archive.net"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename': BASE_DIR + "/logfile.txt",
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'logfile']
    },
}

try:
    from .local import *
except ImportError:
    pass
