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

import re

# The following regexes are from bjweeks' & MZMcBride's snitch.py
# which is public domain
COLOR_RE = re.compile(r'(?:\x02|\x03(?:\d{1,2}(?:,\d{1,2})?)?)')
ACTION_RE = re.compile(r'\[\[(.+)\]\] (?P<log>.+)  \* (?P<user>.+) \*  (?P<summary>.+)')
DIFF_RE = re.compile(r'''
    \[\[(?P<page>.*)\]\]\        # page title
    (?P<patrolled>!|)            # patrolled
    (?P<new>N|)                  # new page
    (?P<minor>M|)                # minor edit
    (?P<bot>B|)\                 # bot edit
    (?P<url>.*)\                 # diff url
    \*\ (?P<user>.*?)\ \*\       # user
    \((?P<diff>(\+|-)\d*)\)\     # diff size
    ?(?P<summary>.*)             # edit summary
''', re.VERBOSE)


def parse_edit(msg):
    msg = COLOR_RE.sub('', msg)
    edit_match = DIFF_RE.match(msg)
    action_match = ACTION_RE.match(msg)
    match = edit_match or action_match
    if not match:
        return
    diff = match.groupdict()
    if not diff['summary']:
        diff['summary'] = '[none]'
    return diff
