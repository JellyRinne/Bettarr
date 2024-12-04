import datetime
import logging
import time
import threading
import redis
import tvdb_v4_official
import configparser

import constants

def getMoviesInitialSync():
    rc1 = redis.Redis(host='localhost', port=6379, db=constants.metadb, charset="utf-8", decode_responses=True)

    rc2 = redis.Redis(host='localhost', port=6379, db=constants.moviesdb, charset="utf-8", decode_responses=True)
    tvdb = tvdb_v4_official.TVDB(constants.tvdb_apikey)

    rc1.set('allMovieInitialSyncStart',str(datetime.datetime.now()))

    page = 0
    while True:
        movies = tvdb.get_all_movies(page=page)
        if (movies != []):
            print('page: ' + str(page))
            for movie in movies:
                rc2.set(movie['id'],str(movie))
            page += 1
            movies = []
        else:
            break
    
    rc2.bgsave()
    rc1.set('allMovieInitialSyncEnd',str(datetime.datetime.now()))
    

getMoviesInitialSync()
