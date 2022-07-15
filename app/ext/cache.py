import os
from flask_caching import Cache
from app.myglobals import cachefolder, cache_expiration

cache = Cache(config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': cachefolder,
    'CACHE_THRESHOLD': 10000,
    'CACHE_DEFAULT_TIMEOUT': cache_expiration,
})
