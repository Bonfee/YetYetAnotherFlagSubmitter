import requests
import socket
import time
from multiprocessing import Process
from backend import MongoConnection
import logging
import logging.config
from config import *


def run(logger):
    global flagcollection
    flagcollection = MongoConnection().db.flags

    while True:
        ids, flags = retrieve()
        if len(ids) > 0:
            # Update retrieved flags' status
            flagcollection.update_many({"_id": {"$in": ids}}, {"$set": {'status': 'pending'}})

            # Submit
            submit(flags, logger)

            # Update submitted flags' status
            flagcollection.update_many({"_id": {"$in": ids}}, {"$set": {'status': 'submitted'}})

        time.sleep(1)


def retrieve():
    ids, flags = [], []

    # Get all the unsubmitted flags,
    # if we want to have many submitter workers we can tweak the number of flags retrieved
    for e in flagcollection.find({'status': 'unsubmitted'}).limit(Config.Submission.flag_limit):
        ids.append(e['_id'])
        flags.append(str(e['flag']))

    return ids, flags


def submit(flags, logger):
    if Config.Submission.protocol == Protocols.plaintext:

        connected = False
        while not connected:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect((Config.Submission.ip, Config.Submission.port))
                connected = True
            except ConnectionRefusedError:
                logger.error('Connection Refused')
                continue

        for flag in flags:
            s.send((flag + '\n').encode())
            # Get response ? ex: flag valid, too old ecc

        s.close()

    elif Config.Submission.protocol == Protocols.Http.get:
        params = {}
        requests.get(Config.Submission.url, params=params)

    elif Config.Submission.protocol == Protocols.Http.post:
        params = {}
        data = {}
        requests.post(Config.Submission.url, params=params, data=data)

    else:
        pass


class Submitter:
    @staticmethod
    def start(logger):
        logger.info('Starting submitter')
        for _ in range(Config.Submission.n_workers):
            Process(target=run, args=(logger,)).start()


if __name__ == '__main__':
    logging.config.fileConfig(fname='log.conf')
    logger = logging.getLogger('submitter')
    Submitter.start(logger)
