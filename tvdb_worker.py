import datetime
import logging
import time
import threading
import redis
import tvdb_v4_official

import constants

def getMoviesInitialSync():
    #connect to meta db
    rc1 = redis.Redis(host='localhost', port=6379, db=constants.metadb, charset="utf-8", decode_responses=True)

    #connect to movies db
    rc2 = redis.Redis(host='localhost', port=6379, db=constants.moviesdb, charset="utf-8", decode_responses=True)
    tvdb = tvdb_v4_official.TVDB(constants.tvdb_apikey)

    #log start time of sync
    rc1.set('allMovieInitialSyncStart',str(datetime.datetime.now()))

    page = 0
    while True:
        movies = tvdb.get_all_movies(page=page)
        if (movies != []):
            for movie in movies:
                rc2.set(movie['id'],str(movie))
            page += 1
            movies = []
        else:
            break

    #save changes to disc
    rc2.bgsave()

    #log end time of initial sync
    rc1.set('allMovieInitialSyncEnd',str(datetime.datetime.now()))
    

getMoviesInitialSync()
