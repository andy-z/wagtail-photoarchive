from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1", "minion", "minion.salnikov.us", "photo-archive.net", "www.photo-archive.net"
]

CSRF_TRUSTED_ORIGINS = ["https://photo-archive.net"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            "formatter": "verbose",
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename': BASE_DIR + "/logfile.txt",
            "formatter": "verbose",
        },
    },
    'root': {
        'level': 'INFO',
        # 'handlers': ['console', 'logfile']
        'handlers': ['console']
    },
}

try:
    from .local import *
except ImportError:
    pass
