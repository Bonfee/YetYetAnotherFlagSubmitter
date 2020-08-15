from exploiter import Exploiter
from webservice import WebService
from submitter import Submitter
import signal

if __name__ == '__main__':
    WebService.start()
    Exploiter.start()
    Submitter.start()
    signal.pause()
