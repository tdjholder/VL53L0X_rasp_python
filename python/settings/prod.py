import os
path = os.path.dirname(os.path.abspath(__file__))
DB_URL = 'sqlite:///' + path + '/sqlite.db'

BREAK_COUNT = 2
READING_INTERVAL = 0.1

