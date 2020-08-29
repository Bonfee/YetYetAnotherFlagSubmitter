from exploiter import Exploiter
from webservice import WebService
from submitter import Submitter
from frontend import Frontend
import signal

if __name__ == '__main__':
    WebService.start()
    Exploiter.start()
    Submitter.start()
    Frontend.start()
    signal.pause()
