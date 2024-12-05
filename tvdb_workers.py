import datetime
import logging
import redis
from redis.commands.json.path import Path
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
                rc2.set(movie['id'],movie)
            page += 1
            movies = []
        else:
            break

    #log end time of initial sync
    rc1.set('allMovieInitialSyncEnd',str(datetime.datetime.now()))

def getUpdateActionUpdateMovies():
    # Connect to meta db
    rc1 = redis.Redis(host='localhost', port=6379, db=constants.metadb, charset="utf-8", 
                      decode_responses=True)

    # Connect to movies db
    rc2 = redis.Redis(host='localhost', port=6379, db=constants.moviesdb, charset="utf-8", 
                      decode_responses=True)
    tvdb = tvdb_v4_official.TVDB(constants.tvdb_apikey)

    # Log start time of sync
    rc1.set('allMovieLastUpdateStart',str(datetime.datetime.now()))

    # Get end of initial movie sync as epoch time, if it's not there, set to 0
    initialSyncEpoch = 0
    if rc1.get('allMovieInitialSyncEnd'):
        dt = datetime.datetime.strptime(rc1.get('allMovieInitialSyncEnd'),constants.date_format)
        initialSyncEpoch = int(dt.timestamp())

    # Get end of last movie update sync as epoch time, if it's not there, set to 0
    lastUpdateEpoch = 0
    if rc1.get('allMovieLastUpdateEnd'):
        dt = datetime.datetime.strptime(rc1.get('allMovieLastUpdateEnd'),constants.date_format)
        lastUpdateEpoch = int(dt.timestamp())
    
    # Retrieve movie updates since that sync time
    page = 0

    while True:
        # Returns a list of updated movies, we still need to actually retrieve the updates
        # later on
        if lastUpdateEpoch > 0:
            movies = tvdb.get_updates(type='movies', action='update', since=lastUpdateEpoch, page=page)
        else:
            movies = tvdb.get_updates(type='movies', action='update', since=initialSyncEpoch, page=page)
        if (movies != []):
            for movie in movies:
                # Here we can retrieve the actual info of the updated movies
                rc2.set(movie['recordId'],str(tvdb.get_movie(movie['recordId'])))
                print(movie)
            page += 1
            movies = []
        else:
            break

    #log end time of sync
    rc1.set('allMovieLastUpdateEnd',str(datetime.datetime.now()))
    
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