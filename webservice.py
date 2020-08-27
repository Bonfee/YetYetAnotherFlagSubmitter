from bson.json_util import dumps
from multiprocessing import Process

import bottle
import re

from config import Config


@bottle.get('/data')
def get_data():
    data = flagcollection.find()
    return dumps(data)


@bottle.post('/submit_many')
def submit_many():
    flags = bottle.request.json.get('flags')
    exploit = bottle.request.json.get('exploit')
    target = bottle.request.json.get('target')

    valid_flags = []
    for f in flags:
        if re.match(Config.Flag.regex, f):
            valid_flags.append(f)
        else:
            print('Regex fail')  # TO DO
            print(f)
            print()

    if len(valid_flags) > 0:
        flagcollection.insert_many(
            [{'flag': flag, 'exploit': exploit, 'target': target, 'status': 'unsubmitted'} for flag in valid_flags])


@bottle.post('/submit')
def submit():
    flag = bottle.request.forms.get('flag')
    exploit = bottle.request.forms.get('exploit')
    target = bottle.request.forms.get('target')

    # Decide whether to send the matched string or the original flag
    if re.match(Config.Flag.regex, flag):
        flagcollection.insert_one({'flag': flag, 'exploit': exploit, 'target': target, 'status': 'unsubmitted'})
    else:
        print('Regex fail')  # TO DO Logging module


def run():
    # Find solution, Process uses fork which would fuck up the MongoClient, maybe start script with exec?
    global flagcollection
    from backend import flagcollection

    bottle.run(host=Config.Backend.WebService.ip, port=Config.Backend.WebService.port, quiet=True)


class WebService:

    @staticmethod
    def start():
        Process(target=run).start()


if __name__ == '__main__':
    WebService.start()
