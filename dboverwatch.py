import datetime
import logging
import time
import threading
import schedule

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

schedule.every(15).minutes.do(every15Minutes)

def runtime():
    while True:
        schedule.run_pending()
        time.sleep(1)

runtime()

