import os
import texttable
import time
from backend import MongoConnection
from config import Config

flagcollection = MongoConnection().db.flags
os.system("clear")
while True:
    table = texttable.Texttable()
    for st in Config.Flag.Status.Manual:
        table.add_row([f"Flag {st.value['text']} (" + str(flagcollection.find({'status': st.value['text']}).count()) + ')'])
    for st in Config.Flag.Status.Returned:
        table.add_row([f"Flag {st.value['text']} (" + str(flagcollection.find({'status': st.value['text']}).count()) + ')'])

    os.system('clear')
    print(table.draw())
    time.sleep(1)
