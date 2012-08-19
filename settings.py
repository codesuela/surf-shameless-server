__author__ = 'Christian'

from os import environ
from urlparse import urlparse

redis_settings = dict()
try:
    redis_con_string = environ["REDISTOGO_URL"]
except KeyError:
    pass
else:
    parsed_url = urlparse(redis_con_string)
    redis_settings = {"host": parsed_url.hostname, "port": parsed_url.port, "password": parsed_url.password}


memcache_settings = dict()
try:
    memcache_servers = [environ["MEMCACHIER_SERVERS"]]
    memcache_settings["username"] = environ["MEMCACHIER_USERNAME"]
    memcache_settings["password"] = environ["MEMCACHIER_PASSWORD"]
except KeyError:
    memcache_servers = ["0.0.0.0"]
