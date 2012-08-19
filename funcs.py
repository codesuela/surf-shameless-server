__author__ = 'Christian'

import pylibmc
import redis
from urlparse import urlparse
import settings

def mc_client():
    return pylibmc.Client(settings.memcache_servers, **settings.memcache_settings)

def redis_client():
    return redis.Redis(**settings.redis_settings)

def truncate_ip(ip):
    # return /24 for ip
    return "_".join(ip.split(".")[:3])

def spam_protect(fn):
    # wrapper to limit the rate at which a /24 subnet can insert new entries
    # counts hits per subnet, raises SpamProtectionStop if over limit
    def protected_function(ip, *args, **kwargs):
        INSERT_LIMIT_PER_RANGE = 30
        EXPIRE_TIME = 60*60

        safe_ip = truncate_ip(ip)
        mc = mc_client()
        submitted_entries_count = mc.get(safe_ip)
        if not submitted_entries_count:
            mc.set(safe_ip, 1, EXPIRE_TIME)
        elif submitted_entries_count >= INSERT_LIMIT_PER_RANGE:
            raise SpamProtectionStop
        mc.incr(safe_ip)

        return fn(ip, *args, **kwargs)
    return protected_function


@spam_protect
def insert_url(ip, url):
    # counts url submissions in redis

    HASH_NAME = "domains"

    url = url.strip()
    parsed_url = urlparse(url)
    if not parsed_url.hostname: return None
    else: hostname = parsed_url.hostname

    if len(hostname) < 60: # dont accept malformed or very long domains
        if hostname[:4] == "www.": #discard www.
            hostname = hostname[4:]

        r = redis_client()
        return r.hincrby(HASH_NAME, hostname)


class SpamProtectionStop(Exception):
    pass
