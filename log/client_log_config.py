import logging


def config_logger():
    logfile = 'log/client.log'
    logging.basicConfig(
        filename=logfile,
        format='%(asctime)s %(levelname)s %(module)s %(message)s',
        level=logging.DEBUG)

    return logging.getLogger('server_log')
