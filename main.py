from exploiter import Exploiter
from webservice import WebService
from submitter import Submitter
from frontend import Frontend
import signal
import logging.config

if __name__ == '__main__':
    logging.config.fileConfig(fname='log.conf')
    logger_exploiter = logging.getLogger('exploiter')
    logger_submitter = logging.getLogger('submitter')
    logger_webservice = logging.getLogger('webservice')

    WebService.start(logger_webservice)
    Exploiter.start(logger_exploiter)
    Submitter.start(logger_submitter)
    Frontend.start()

    signal.pause()
