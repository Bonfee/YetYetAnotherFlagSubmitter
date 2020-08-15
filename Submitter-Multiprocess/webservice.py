import bottle
from config import Config
from multiprocessing import Process


@bottle.post('/submit')
def submit():
    flag = bottle.request.forms.get('flag')
    exploit = bottle.request.forms.get('exploit')
    target = bottle.request.forms.get('target')

    flagcollection.insert_one({'flag': flag, 'exploit': exploit, 'target': target, 'status': 'unsubmitted'})


def run():
    # Find solution, Process uses fork which would fuck up the MongoClient, maybe start script with exec?
    from backend import flagcollection
    global flagcollection

    bottle.run(host=Config.Backend.WebService.ip, port=Config.Backend.WebService.port, quiet=True)


class WebService:

    @staticmethod
    def start():
        Process(target=run).start()


if __name__ == '__main__':
    WebService.start()
