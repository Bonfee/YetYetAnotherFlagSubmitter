import os
import texttable
import time

from backend import *

os.system("clear")
while True:
    table = texttable.Texttable()
    #    table.add_row(['Flag', 'Exploit', 'Target'])
    #    for e in flagcollection.find():
    #        table.add_row([e['flag'], e['exploit'], e['target']])
    table.add_row(['Flag Unsubmitted (' + str(flagcollection.find({'status': 'unsubmitted'}).count()) + ')'])
    table.add_row(['Flag Pending (' + str(flagcollection.find({'status': 'pending'}).count()) + ')'])
    table.add_row(['Flag Submitted (' + str(flagcollection.find({'status': 'submitted'}).count()) + ')'])
    os.system('clear')
    print(table.draw())
    time.sleep(1)
