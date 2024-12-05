import datetime
import logging
import time
import threading
import redis
import tvdb_v4_official

import constants

def getMoviesInitialSync():
    #connect to meta db
    rc1 = redis.Redis(host='localhost', port=6379, db=constants.metadb, charset="utf-8", 
                      decode_responses=True)

    #connect to movies db
    rc2 = redis.Redis(host='localhost', port=6379, db=constants.moviesdb, charset="utf-8", 
                      decode_responses=True)
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

    #log end time of initial sync
    rc1.set('allMovieInitialSyncEnd',str(datetime.datetime.now()))

def getUpdateActionUpdateMovies():
    #connect to meta db
    rc1 = redis.Redis(host='localhost', port=6379, db=constants.metadb, charset="utf-8", 
                      decode_responses=True)

    #connect to movies db
    rc2 = redis.Redis(host='localhost', port=6379, db=constants.moviesdb, charset="utf-8", 
                      decode_responses=True)
    tvdb = tvdb_v4_official.TVDB(constants.tvdb_apikey)

    #log start time of sync
    rc1.set('allMovieLastUpdateStart',str(datetime.datetime.now()))

    #get end of initial movie sync as epoch time
    dt = datetime.datetime.strptime(rc1.get('allMovieInitialSyncEnd'),constants.date_format)
    lastUpdateEpoch = int(dt.timestamp())
    
    #retrieve movie updates since that sync time
    page = 0

    while True:
        movies = tvdb.get_updates(action='update', since=lastUpdateEpoch, page=page)
        if (movies != []):
            for movie in movies:
                rc2.set(movie['id'],str(movie))
            page += 1
            movies = []
        else:
            break

    #log end time of sync
    rc1.set('allMovieLastUpdateStart',str(datetime.datetime.now()))
    
#getMoviesInitialSync()
getUpdateActionUpdateMovies()

    













#getMoviesInitialSync()

#def getMoviesTestFailure():
#    tvdb = tvdb_v4_official.TVDB(constants.tvdb_apikey)
#    movies = []
#    movies = tvdb.get_all_movies(page=999)
#
#    print(str(movies))

#getMoviesTestFailure()

# returns empty array as expected