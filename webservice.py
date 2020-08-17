from bson.json_util import dumps
import re
from multiprocessing import Process

import bottle

from config import Config


@bottle.get('/data')
def get_data():
    data = flagcollection.find()
    return dumps(data)


@bottle.post('/submit')
def submit():
    flag = bottle.request.forms.get('flag')
    exploit = bottle.request.forms.get('exploit')
    target = bottle.request.forms.get('target')

    # Decide whether to send the matched string or the original flag
    if re.match(Config.Flag.regex, flag):
        flagcollection.insert_one({'flag': flag, 'exploit': exploit, 'target': target, 'status': 'unsubmitted'})


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
