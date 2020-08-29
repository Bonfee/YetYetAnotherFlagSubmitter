import re
from multiprocessing import Process
import bottle
from bson.json_util import dumps
from backend import MongoConnection
from config import Config


@bottle.get('/data')
def get_data():
    data = flagcollection.find()
    return dumps(data)


@bottle.post('/submit_many')
def submit_many():
    flags = bottle.request.json.get('flags')
    exploit = bottle.request.json.get('exploit')
    timestamp = bottle.request.forms.get('timestamp')
    target = bottle.request.json.get('target')

    valid_flags = []
    for f in flags:
        if re.match(Config.Flag.regex, f):
            valid_flags.append(f)
        else:
            print('Regex fail')  # TO DO
            return bottle.HTTPResponse({'error': 'Flag was not correct'}, 400)

    if len(valid_flags) > 0:
        flagcollection.insert_many([{'flag': flag, 'exploit': exploit, 'target': target, 'timestamp': timestamp,
                                     'status': 'unsubmitted'} for flag in valid_flags])


@bottle.post('/submit')
def submit():
    flag = bottle.request.forms.get('flag')
    exploit = bottle.request.forms.get('exploit')
    timestamp = bottle.request.forms.get('timestamp')
    target = bottle.request.forms.get('target')

    # Decide whether to send the matched string or the original flag
    if re.match(Config.Flag.regex, flag):
        flagcollection.insert_one({'flag': flag, 'exploit': exploit, 'target': target, 'timestamp': timestamp,
                                   'status': 'unsubmitted'})
    else:
        print('Regex fail')  # TO DO
        return bottle.HTTPResponse({'error': 'Flag was not correct'}, 400)


def run():
    global flagcollection
    flagcollection = MongoConnection().db.flags

    bottle.run(host=Config.Backend.WebService.ip, port=Config.Backend.WebService.port, server='bjoern', quiet=True)


class WebService:

    @staticmethod
    def start():
        Process(target=run).start()


if __name__ == '__main__':
    WebService.start()
