import pathlib, pytz
from datetime import datetime


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
        class WebService:
            ip = '127.0.0.1'
            port = 8080
            url_submit = 'http://%s:%d/submit' % (ip, port)
            url_submit_many = 'http://%s:%d/submit_many' % (ip, port)

    class Flag:
        regex = r'CCIT{.*}'

    class Redis:
        ip = "127.0.0.1"
        port = 6379
        channel = "flags"

    exploits_dir = str(pathlib.Path(__file__).parent.absolute()) + '/exploits'
    targets_file = str(pathlib.Path(__file__).parent.absolute()) + '/targets.txt'
    team_ip = '23.10.2.221'
