from multiprocessing import Process
import bottle
import json
from mongo_datatables import DataTables
from backend import MongoConnection
from config import Config
from util import get_exploits


# Home page
@bottle.route('/')
def index():
    return bottle.template('tables.tpl')


# Serve static files
@bottle.route('/vendor/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/vendor')


@bottle.route('/js/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/js')


@bottle.route('/css/:filename#.*#')
def send_static(filename):
    return bottle.static_file(filename, root='./static/css')


# DataTables Ajax handler
@bottle.route('/table_ajax/<collection>')
def api_db(collection):
    mongo = MongoConnection()
    request_args = json.loads(bottle.request.query.get("args"))
    results = DataTables(mongo, collection, request_args).get_rows()
    return json.dumps(results)


# Pie Chart Ajax
@bottle.route('/dispatching_ajax')
def get_stats():
    mongo = MongoConnection()
    data = {}

    for st in Config.Flag.Status.Manual:
        flag_status = st.value['text']
        data[flag_status] = mongo.db.flags.find({'status': flag_status}).count()

    for st in Config.Flag.Status.Returned:
        flag_status = st.value['text']
        data[flag_status] = mongo.db.flags.find({'status': flag_status}).count()

    return json.dumps(data)


# Bar Chart Ajax
@bottle.route('/barchart_ajax')
def get_stats():
    exploits = get_exploits()
    labels = []
    count = []
    for exploit in exploits:
        flagno = MongoConnection().db.flags.find({'exploit': exploit}).count()
        count.append(flagno)
        exploit_name = exploit.split('/')
        exploit_name = exploit_name[-1]
        labels.append(exploit_name)
    return json.dumps({'labels': labels, 'count': count})


def run():
    bottle.run(host=Config.Frontend.ip, port=Config.Frontend.port, server='bjoern', quiet=True)


class Frontend:

    @staticmethod
    def start():
        Process(target=run).start()


if __name__ == '__main__':
    Frontend.start()
