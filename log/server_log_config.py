"""
В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:
Создание именованного логгера;
Сообщения лога должны иметь следующий формат:
"<дата-время> <уровень_важности> <имя_модуля> <сообщение>";
Журналирование должно производиться в лог-файл;

На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
Реализовать применение созданных логгеров для решения двух задач:
Журналирование обработки исключений try/except.
Вместо функции print() использовать журналирование и обеспечить вывод служебных сообщений в лог-файл;
Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.

"""

import logging
from logging.handlers import TimedRotatingFileHandler


def config_logger():
    logfile = 'log/server.log'
    logging.basicConfig(
        filename=logfile,
        format='%(asctime)s %(levelname)s %(module)s %(message)s',
        level=logging.DEBUG)

    log = logging.getLogger('server_log')
    rotator = logging.getLogger('rotating log')
    rotate_handler = TimedRotatingFileHandler(logfile, when='D', interval=1)

    # I get double messaging in log if use
    # log.addHandler(rotate_handler)
    rotator.addHandler(rotate_handler)

    return log
