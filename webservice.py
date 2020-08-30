from bson.json_util import dumps
from multiprocessing import Process

import bottle, json, random
import re

from config import Config
from mongo_datatables import DataTables
from pymongo import *
from util import get_exploits
#Initialize new mongo connection, adapted to Flask standards. As suggested by mongo docs, one connection per child.
class MongoConnection(object):

    def __init__(self):
        client = MongoClient(Config.Backend.Mongo.ip, Config.Backend.Mongo.port)
        self.db = client['submitter_db']

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
    IP = bottle.request.forms.get('IP')
    timestamp = bottle.request.forms.get('timestamp')
    target = bottle.request.forms.get('target')

    # Decide whether to send the matched string or the original flag
    if re.match(Config.Flag.regex, flag):
        flagcollection.insert_one({'flag': flag, 'exploit': exploit, 'target': target, 'IP':IP, 'timestamp':timestamp, 'target':target, 'status': 'unsubmitted'})
    else:
        print('Regex fail')  # TO DO
        return bottle.HTTPResponse({'error': 'Flag was not correct'}, 400)



def run():
    # Find solution, Process uses fork which would fuck up the MongoClient, maybe start script with exec?
    global flagcollection
    from backend import flagcollection

    bottle.run(host=Config.Backend.Bottle.ip, port=Config.Backend.Bottle.port, quiet=True)


class WebService:

    @staticmethod
    def start(logger):
        logger.info('Starting webservice')
        Process(target=run).start()


if __name__ == '__main__':
    logging.config.fileConfig(fname='log.conf')
    logger = logging.getLogger('webservice')
    WebService.start(logger)
    
#Bottle routes
#Home page
@bottle.route('/')
def index():
   
    return bottle.template('tables.tpl')
#Serve static files    
@bottle.route('/vendor/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/vendor')

@bottle.route('/js/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/js')

@bottle.route('/css/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/css')
#DataTables Ajax handler    
@bottle.route('/table_ajax/<collection>')
def api_db(collection):
    mongo = MongoConnection()
    request_args = json.loads(bottle.request.query.get("args"))
    results = DataTables(mongo, collection, request_args).get_rows()
    return json.dumps(results)
#Pie Chart Ajax
@bottle.route('/dispatching_ajax')
def get_stats(): 
    failed = flagcollection.find({'status': 'failed'}).count()
    submitted = flagcollection.find({'status': 'submitted'}).count()
    unsubmitted = flagcollection.find({'status': 'unsubmitted'}).count()
    pending = flagcollection.find({'status': 'pending'}).count()
    return json.dumps({'failed':failed,'submitted':submitted,'pending':pending, 'unsubmitted':unsubmitted})
#Bar Chart Ajax
@bottle.route('/barchart_ajax')
def get_stats(): 
    exploits = get_exploits()
    labels = []
    count = []
    for exploit in exploits:
        flagno = flagcollection.find({'exploit': exploit}).count()
        count.append(flagno);
        exploit_name = exploit.split('/')
        exploit_name = exploit_name[-1]
        labels.append(exploit_name)
    return json.dumps({'labels':labels,'count':count})

