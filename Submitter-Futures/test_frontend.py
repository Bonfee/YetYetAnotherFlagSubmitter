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
    table.add_row(['Flag('+str(flagcollection.estimated_document_count())+')', 'Exploit', 'Target'])
    os.system('clear')
    print(table.draw())
    time.sleep(1)
