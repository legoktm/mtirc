#!/usr/bin/env python
import cPickle
try:
    import memcache
except ImportError:
    memcache = False
import os
import sys


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

    def __contains__(self, item):
        if self.use_mc:
            return self.mc.get(item) is not None
        else:
            return item in self.d

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.d = cPickle.load(f)
        else:
            self.d = {}

    def save(self):
        with open(self.filename, 'w') as f:
            cPickle.dump(self.d, f)

    def get(self, key):
        if self.use_mc:
            return self.mc.get(str(key))
        return self.d[key]

    def set(self, key, value, save=True):
        if self.use_mc:
            self.mc.set(str(key), value)
            return
        self.d[key] = value
        if save:
            self.save()

    def delete(self, key, save=True):
        if self.use_mc:
            self.mc.delete(str(key))
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
    print repr(mc[str(sys.argv[1])])
