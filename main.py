from exploiter import Exploiter
from webservice import WebService
import signal
import logging.config

if __name__ == '__main__':
    logging.config.fileConfig(fname='log.conf')
    logger_exploiter = logging.getLogger('exploiter')
    logger_webservice = logging.getLogger('webservice')

    WebService.start(logger_webservice)
    Exploiter.start(logger_exploiter)

    signal.pause()
