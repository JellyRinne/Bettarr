import datetime
import logging
import time
import threading
import redis
import tvdb_v4_official

import constants

rc = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)
tvdb = tvdb_v4_official.TVDB(constants.tvdb_apikey)

testval = 11317

movie = tvdb.get_movie(testval)

print('::::::MOVIE FROM TVDB::::::')
print(movie)

rc.set(testval, str(movie))

print('::::::MOVIE FROM REDIS::::::')
print(rc.get(testval))
