#!/usr/bin/env python
"""
Copyright (C) 2013 Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""


import unittest

from mtirc import bot
from mtirc import cache
from mtirc import settings


class CacheTests(unittest.TestCase):

    def setUp(self):
        config = settings.config
        config['nick'] = 'unittestbot'
        config['use_memcache'] = False
        config['connections']['card.freenode.net']['channels'] = ['#bottest']
        self.bot = bot.Bot(config)

    def test_file_cache(self):
        config = dict(settings.config)
        config['use_memcache'] = False
        mc = cache.Cache(config)
        mc.set('123', 'test')
        self.assertEqual(mc.get('123'), 'test')
        self.assertTrue('123' in mc)
        self.assertEqual(mc.dump(), {'123': 'test', u'errors': {}})
        mc.delete('123')
        self.assertFalse('123' in mc)

    def test_memcache_cache(self):
        config = dict(settings.config)
        config['use_memcache'] = True
        mc = cache.Cache(config)
        self.assertTrue(mc.use_mc)  # This ensures that we're actually using memcache, not file cache
        mc.set('123', 'test')
        self.assertEqual(mc.get('123'), 'test')
        self.assertTrue('123' in mc)
        mc.delete('123')
        self.assertFalse('123' in mc)


if __name__ == "__main__":
    unittest.main()
