import requests
import socket
import time
from multiprocessing import Process
from backend import MongoConnection
import logging
import logging.config
from config import *
from util import get_flag_status, insert_flag


def run(logger):
    while True:
        ids, flags = retrieve()
        if len(ids) > 0:
            # Update retrieved flags' status
            MongoConnection().db.flags.update_many({"_id": {"$in": ids}},
                                                   {"$set": {'status': Config.Flag.Status.Manual.pending.value['text']}})

            # Submit
            status = submit(flags, logger)

            # Update submitted flags' status
            for i in range(0, len(ids)):
                MongoConnection().db.flags.update_one({"_id": ids[i]}, {"$set": {'status': status[i]}})

        time.sleep(1)


def retrieve():
    ids, flags = [], []

    # Get all the unsubmitted flags,
    # if we want to have many submitter workers we can tweak the number of flags retrieved
    for e in MongoConnection().db.flags.find({'status': Config.Flag.Status.Manual.unsubmitted.value['text']}
                                             ).limit(Config.Submission.flag_limit):
        ids.append(e['_id'])
        flags.append(str(e['flag']))

    return ids, flags


def submit(flags, logger):
    status = []

    if Config.Submission.protocol == Protocols.plaintext:

        connected = False
        while not connected:
            if(Config.Submission.use_ipv6):
                addrfamily = socket.AF_INET6
            else:
                addrfamily = socket.AF_INET

            s = socket.socket(addrfamily, socket.SOCK_STREAM)

            try:
                s.connect((Config.Submission.ip, Config.Submission.port))
                connected = True
            except ConnectionRefusedError:
                logger.error('Connection Refused')
                continue

        for flag in flags:
            s.send((flag + '\n').encode())
            output = s.recv(4096).decode()

            status.append(get_flag_status(output))

        s.close()

    elif Config.Submission.protocol == Protocols.Http.get:
        for flag in flags:
            r = requests.get(Config.Submission.url, params=Config.Submission.params)
            output = r.text.strip()
            status.append(get_flag_status(output))

    elif Config.Submission.protocol == Protocols.Http.post:
        for flag in flags:
            data = insert_flag(Config.Submission.data,
                               flag)  # Replace 'flag' value in Config.Submission.data with the real flag
            r = requests.post(Config.Submission.url, params=Config.Submission.params, data=data)
            output = r.text.strip()
            status.append(get_flag_status(output))

    else:
        pass

    return status


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
