
import logging
import logging.handlers
import logging.config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Настройки почтового сервера
EMAIL_HOST = 'smtp.example.com'
EMAIL_PORT = 587
EMAIL_USER = 'user@example.com'
EMAIL_PASSWORD = 'password'
EMAIL_RECEIVER = 'receiver@example.com'

# Функция для отправки почтового сообщения
def send_email(message):
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_USER, EMAIL_RECEIVER, message.as_string())
    server.quit()

# Создаем логгеры
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console_formatter': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
        'file_formatter': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        },
        'error_formatter': {
            'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s\n%(exc_info)s'
        },
        'security_formatter': {
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
        }
    },
    'handlers': {
        'console_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console_formatter'
        },
        'file_general_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'file_formatter',
            'filename': 'general.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
        'file_errors_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'error_formatter',
            'filename': 'errors.log',
            'maxBytes': 1024,
            'backupCount': 3
        },
        'file_security_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'security_formatter',
            'filename': 'security.log',
            'maxBytes': 1024,
            'backupCount': 3
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_handler', 'file_general_handler', 'file_errors_handler', 'file_security_handler'],
            'level': 'DEBUG'
        }
    }
})


# Создаем фильтры для почты и файлов
class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

class ProductionFilter(logging.Filter):
    def filter(self, record):
        return record.levelno >= logging.ERROR

# Применяем фильтры к обработчикам
console_handler = logging.getLogger().handlers[0]
console_handler.addFilter(DebugFilter())

file_general_handler = logging.getLogger().handlers[1]
file_errors_handler = logging.getLogger().handlers[2]
file_security_handler = logging.getLogger().handlers[3]

file_general_handler.addFilter(ProductionFilter())
file_errors_handler.addFilter(ProductionFilter())
file_security_handler.addFilter(ProductionFilter())

# Пример логирования
logger = logging.getLogger('django')

logger.debug('Debug message')
logger.info('Info message')
logger.warning('Warning message')
logger.error('Error message')
logger.critical('Critical message')