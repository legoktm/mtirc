#!/usr/bin/env python

from __future__ import print_function

import os
import six
import sys
try:
    import memcache
except ImportError:
    memcache = False
try:
    import cPickle as pickle
except ImportError:
    import pickle

# The point of this module is so we can easily
# transition between systems that have memcache
# installed and those that don't


class Cache:
    def __init__(self, config):
        self.config = config
        self.use_mc = memcache and self.config['use_memcache']
        if self.use_mc:
            self.mc = memcache.Client([self.config['mc_host']])
        else:
            self.mc = None
        self.filename = self.config['cache_file'] + '.cache'
        self.load()

    def __contains__(self, key):
        key = six.u(key)
        if self.use_mc:
            return self.mc.get(key) is not None
        else:
            return key in self.d

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
        key = six.u(key)
        if self.use_mc:
            return self.mc.get(key)
        return self.d[key]

    def set(self, key, value, save=True):
        key = six.u(key)
        if self.use_mc:
            self.mc.set(key, value)
            return
        self.d[key] = value
        if save:
            self.save()

    def delete(self, key, save=True):
        key = six.u(key)
        if self.use_mc:
            self.mc.delete(key)
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
