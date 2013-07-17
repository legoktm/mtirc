#!/usr/bin/env python

from __future__ import print_function

import sys
import os
try:
    import memcache
except ImportError:
    memcache = False
try:
    import redis
except ImportError:
    redis = False
try:
    import cPickle as pickle
except ImportError:
    import pickle

import settings  # For constants

# The point of this module is so we can easily
# transition between systems that have memcache
# installed and those that don't


class Cache:
    def __init__(self, config):
        """
        config is settings.config['cache'], not the entire
        config file.
        """
        self.config = config
        self.type = self.config['type']
        if self.type == settings.CACHE_MEMCACHE and memcache:
            self.thing = memcache.Client([self.config['host']])
        elif self.type == settings.CACHE_REDIS and redis:
            self.thing = redis.StrictRedis(host=self.config['host'], port=self.config['port'])
        else:
            self.thing = None
        self.filename = self.config['cache_file'] + '.cache'
        self.load()

    def __contains__(self, item):
        if self.thing:
            return self.thing.get(item) is not None
        else:
            return item in self.d

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                self.d = pickle.load(f)
        else:
            self.d = {}

    def save(self):
        with open(self.filename, 'w') as f:
            pickle.dump(self.d, f)

    def get(self, key):
        if self.thing:
            return self.thing.get(str(key))
        return self.d[key]

    def set(self, key, value, save=True):
        if self.thing:
            self.thing.set(str(key), value)
            return
        self.d[key] = value
        if save:
            self.save()

    def delete(self, key, save=True):
        if self.thing:
            self.thing.delete(str(key))
            return
        del self.d[key]
        if save:
            self.save()

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, item):
        return self.get(item)

    def __delitem__(self, key):
        self.delete(key)

    def dump(self):
        return self.d

if __name__ == "__main__":
    # for easy debugging:
    from mtirc import settings
    mc = Cache(settings.config)
    print(repr(mc[str(sys.argv[1])]))
