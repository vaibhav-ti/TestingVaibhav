# Logging

Django uses and extends Python’s builtin [logging](https://docs.python.org/3/library/logging.html#module-logging) module to perform system logging

### Loggers
A logger is the entry point into the logging system. Each logger is a named bucket to which messages can be written for processing.

A logger is configured to have a log level. This log level describes the severity of the messages that the logger will handle. Python defines the following log levels:

- **DEBUG**: Low level system information for debugging purposes
- **INFO**: General system information
- **WARNING**: Information describing a minor problem that has occurred.
- **ERROR**: Information describing a major problem that has occurred.
- **CRITICAL**: Information describing a critical problem that has occurred.
Each message that is written to the logger is a Log Record. Each log record also has a log level indicating the severity of that specific message. A log record can also contain useful metadata that describes the event that is being logged. This can include details such as a stack trace or an error code.

When a message is given to the logger, the log level of the message is compared to the log level of the logger. If the log level of the message meets or exceeds the log level of the logger itself, the message will undergo further processing. If it doesn’t, the message will be ignored.

Once a logger has determined that a message needs to be processed, it is passed to a Handler.

### Handlers

The handler is the engine that determines what happens to each message in a logger. It describes a particular logging behavior, such as writing a message to the screen, to a file, or to a network socket.

Like loggers, handlers also have a log level. If the log level of a log record doesn’t meet or exceed the level of the handler, the handler will ignore the message.

A logger can have multiple handlers, and each handler can have a different log level. In this way, it is possible to provide different forms of notification depending on the importance of a message. For example, you could install one handler that forwards **ERROR** and **CRITICAL** messages to a paging service, while a second handler logs all messages (including **ERROR** and **CRITICAL** messages) to a file for later analysis.

### Filters

A filter is used to provide additional control over which log records are passed from logger to handler.

By default, any log message that meets log level requirements will be handled. However, by installing a filter, you can place additional criteria on the logging process. For example, you could install a filter that only allows **ERROR** messages from a particular source to be emitted.

Filters can also be used to modify the logging record prior to being emitted. For example, you could write a filter that downgrades **ERROR** log records to **WARNING** records if a particular set of criteria are met.

Filters can be installed on loggers or on handlers; multiple filters can be used in a chain to perform multiple filtering actions.

### Formatters
Ultimately, a log record needs to be rendered as text. Formatters describe the exact format of that text. A formatter usually consists of a Python formatting string containing LogRecord attributes; however, you can also write custom formatters to implement specific formatting behavior.

## Configuring logging

By default, the LOGGING setting is merged with Django’s default logging configuration using the following scheme.

The full documentation for [dictConfig format](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema) is the best source of information about logging configuration dictionaries. 

```python
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
            'level': os.getenv('CONSOLE_LOG_LEVEL', 'DEBUG'),
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
        'myproject': {
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
```

[More Details](https://docs.djangoproject.com/en/4.1/topics/logging/)
