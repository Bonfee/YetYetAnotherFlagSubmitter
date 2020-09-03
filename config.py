import pathlib, pytz
from datetime import datetime
from enum import Enum


class Protocols:
    plaintext = 0

    class Http:
        get = 1
        post = 2


class Config:
    class CTF:
        tick = 120  # round length in seconds
        start = pytz.timezone('Europe/Rome') \
            .localize(datetime(year=2020, month=9, day=4, hour=10, minute=30)) \
            .astimezone(pytz.timezone('UTC')) \
            .timestamp()

    class Exploiter:
        PoolSize = 200
        timeout = 30

        # To specify a custom exploit just add an entry with the exploit file name without the extension
        class CustomTimeouts:
            exploit1 = 10

    class Backend:
        class Mongo:
            ip = '127.0.0.1'
            port = 27017

        class WebService:
            ip = '0.0.0.0'
            port = 8080
            url_submit = 'http://%s:%d/submit' % (ip, port)
            url_submit_many = 'http://%s:%d/submit_many' % (ip, port)

    class Frontend:
        # needed for docker
        ip = '0.0.0.0'
        port = 8000

    class Flag:
        regex = r'CCIT{.*}'

        # This class represent the status of flags in the database
        # text -> The string that will be stored in the database and displayed in the frontend
        # match -> The response of the gameserver when submitting the flag
        class Status:
            class Returned(Enum):  # Status returned from the gameserver
                valid = {
                    'text': 'Valid',
                    'match': 'valid flag'
                }
                too_old = {
                    'text': 'Too old',
                    'match': 'too old flag'
                }
                already_submitted = {
                    'text': 'Already submitted',
                    'match': 'flag already submitted'
                }
                invalid = {
                    'text': 'Invalid flag',
                    'match': 'flag is invalid'
                }

            class Manual(Enum):
                unknown = {
                    'text': 'Unknown'  # If the server returns something we didn't expect
                }
                unsubmitted = {
                    'text': 'Unsubmitted'
                }
                pending = {
                    'text': 'Pending'
                }

    class Submission:
        ip = "127.0.0.1"
        port = 1234
        protocol = Protocols.plaintext
        url = "http://%s:%d/" % (ip, port)
        n_workers = 5
        flag_limit = 50

        data = {
            'data1': 'value1'
        }  # POST request data
        params = {
            'param1': 'value1'
        }  # POST and GET request params

    exploits_dir = str(pathlib.Path(__file__).parent.absolute()) + '/exploits'
    targets_file = str(pathlib.Path(__file__).parent.absolute()) + '/targets.txt'
    team_ip = '23.10.2.221'
