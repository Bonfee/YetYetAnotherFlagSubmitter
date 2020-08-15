import pathlib


class Protocols:
    plaintext = 0

    class Http:
        get = 1
        post = 2


class Config:
    class Exploiter:
        PoolSize = 200

    class Backend:
        class Mongo:
            ip = '127.0.0.1'
            port = 27017

        class WebService:
            ip = '127.0.0.1'
            port = 8080
            url_submit = 'http://%s:%d/submit' % (ip, port)

    class Flag:
        regex = r'FLAG{.*}'

    class Submission:
        ip = "127.0.0.1"
        port = 1234
        protocol = Protocols.plaintext
        url = "http://%s:%d/" % (ip, port)

    exploits_dir = str(pathlib.Path(__file__).parent.absolute()) + '/exploits'
    targets_file = str(pathlib.Path(__file__).parent.absolute()) + '/targets.txt'
    team_ip = '23.10.2.221'
