from exploiter import Exploiter
from webservice import WebService
import signal, time

if __name__ == '__main__':
    WebService.start()
    Exploiter.start()
    signal.pause()
