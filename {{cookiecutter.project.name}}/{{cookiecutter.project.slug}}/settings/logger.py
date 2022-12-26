import os
import sys
import logging

logger = logging.getLogger(__name__)


# Logging
class LoggingExcludeModulesFilter(logging.Filter):
    """Exclude modules from logging"""

    def __init__(self, modules_list=None):
        super().__init__()
        self.modules_list = modules_list

    def filter(self, record):
        return record.module not in self.modules_list


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'exclude_modules': {
            '()': LoggingExcludeModulesFilter,
            'modules_list': ['autoreload', 'hooks'],
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] [%(module)s.%(funcName)s] %(message)s'
        },
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
        },
        'simple': {
            'format': '[%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
        },
        'request': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': os.getenv('CONSOLE_LOG_LEVEL', 'ERROR'),
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        },
        'request-console': {
            'level': 'INFO',
            'formatter': 'request',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        '{{cookiecutter.project.slug}}': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,  # required to avoid double logging with root logger
        },
        'tests': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,  # required to avoid double logging with root logger
        },
        'django': {
            'handlers': ['request-console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}