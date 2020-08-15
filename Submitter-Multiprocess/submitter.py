import socket
from threading import Thread

import re
import requests
from config import *


class SubmitterThread(Thread):

    def __init__(self, flag):
        Thread.__init__(self)
        self.flag = flag

    def run(self):
        if Config.Submission.protocol == Protocols.plaintext:

            connected = False
            while not connected:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((Config.Submission.ip, Config.Submission.port))
                    connected = True
                except ConnectionRefusedError:
                    continue

            s.send((self.flag + '\n').encode())
            s.close()

        elif Config.Submission.protocol == Protocols.Http.get:
            params = {}
            r = requests.get(Config.Submission.url, params=params)

        elif Config.Submission.protocol == Protocols.Http.post:
            params = {}
            data = {}
            r = requests.post(Config.Submission.url, params=params, data=data)

        else:
            pass


class Submitter:
    def __init__(self, flag):
        # Decide whether to send the matched string or the original flag
        if re.match(Config.Flag.regex, flag):
            s = SubmitterThread(flag)
            s.start()
        else:
            # LOG invalid flag
            pass
