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
from mtirc import lib
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
        #self.assertTrue(mc.use_mc)  # This ensures that we're actually using memcache, not file cache
        # Except it doesn't work in py3k....
        mc.set('123', 'test')
        self.assertEqual(mc.get('123'), 'test')
        self.assertTrue('123' in mc)
        mc.delete('123')
        self.assertFalse('123' in mc)


class LibTests(unittest.TestCase):

    def setUp(self):
        self.edit = u'\x0314[[\x0307Hassan Rouhani\x0314]]\x034 \x0310 \x0302http://en.wikipedia.org/w/index.php?diff=560860840&oldid=560857945\x03 \x035*\x03 \x030337.98.125.156\x03 \x035*\x03 (+179) \x0310/* After the Islamic Revolution */\x03'
        self.action = u'\x0314[[\x0307Special:Log/abusefilter\x0314]]\x034 hit\x0310 \x0302\x03 \x035*\x03 \x030382.93.10.193\x03 \x035*\x03  \x031082.93.10.193 triggered [[Special:AbuseFilter/260|filter 260]], performing the action "edit" on [[\x0302Jack Dorsey\x0310]]. Actions taken: Disallow ([[Special:AbuseLog/8932011|details]])\x03'

    def test_color_stripping(self):
        self.assertEqual(lib.COLOR_RE.sub('', self.edit), u'[[Hassan Rouhani]]  http://en.wikipedia.org/w/index.php?diff=560860840&oldid=560857945 * 37.98.125.156 * (+179) /* After the Islamic Revolution */')

    def test_edit_parsing(self):
        self.assertEqual(lib.parse_edit(self.edit), {'url': u'http://en.wikipedia.org/w/index.php?diff=560860840&oldid=560857945', 'bot': u'', 'summary': u'/* After the Islamic Revolution */', 'user': u'37.98.125.156', 'new': u'', 'diff': u'+179', 'patrolled': u'', 'page': u'Hassan Rouhani', 'minor': u''})

    def test_action_parsing(self):
        self.assertEqual(lib.parse_edit(self.action), {'user': u'82.93.10.193', 'log': u'hit', 'summary': u'82.93.10.193 triggered [[Special:AbuseFilter/260|filter 260]], performing the action "edit" on [[Jack Dorsey]]. Actions taken: Disallow ([[Special:AbuseLog/8932011|details]])'})

if __name__ == "__main__":
    unittest.main()
