import datetime
import logging
import time
import threading
import redis
import tvdb_v4_official

import constants

tvdb = tvdb_v4_official.TVDB(constants.tvdb_apikey)