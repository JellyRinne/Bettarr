import datetime
import logging
import time
import schedule
import redis

import constants

logger = logging.getLogger(__name__)
logging.basicConfig(filename='dboverwatch.log', encoding='utf-8', level=logging.DEBUG)
logging.info(str(datetime.datetime.now()) + ' - SESSION STARTED')

# Import local modules
import tvdb_workers

# Define queues
def setup():
    tvdb_workers.getMoviesInitialSync

def every15Minutes():
    tvdb_workers.getUpdateActionUpdateMovies

# Schedule queues
schedule.every(15).minutes.do(every15Minutes)

def runtime():
    #connect to meta db
    rc1 = redis.Redis(host='localhost', port=6379, db=constants.metadb, charset="utf-8", 
                      decode_responses=True)
    
    # Check for a finished Initial All Movies Sync. If we don't have one, run setup syncs
    if not rc1.get('allMovieInitialSyncEnd'):
        setup()

    # Start runtime of scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

#runtime()

