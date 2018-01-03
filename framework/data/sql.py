import os
import json
import sqlalchemy
import pandas as pd
from threading import Thread
from subprocess import Popen, PIPE

def sql(db): return sqlalchemy.create_engine(
    json.load(
        open(os.path.expanduser('~/.sql.conf'), 'r'))['uri'] + db)

def sql_to_csv(query, *args, script='%s/sql_to_csv.sh' % (os.path.abspath(os.path.dirname(__file__)))):
    ''' We execute this script in another thread after getting the temporary fifo and returning it
    that fifo can then be treated as a file for the output of the provided query. '''
    p = Popen([script, *args], stdin=PIPE, stdout=PIPE)
    f = p.stdout.readline().strip().decode()
    t = Thread(target=p.communicate, kwargs={'input': query.encode()})
    t.start()
    return f
