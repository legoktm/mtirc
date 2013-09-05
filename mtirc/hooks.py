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
----
Implements a proper hooking system so any module
can hook up at different points.
"""

import logging
import traceback
hooks = {}


def add_hook(event_name, mod_name, func):
    data = {'run': func, 'disabled': 0}
    if event_name in hooks:
        hooks[event_name][mod_name] = data
    else:
        hooks[event_name] = {mod_name: data}


def run_event(name, **kw):
    if name in hooks:
        for mod_name in hooks[name]:
            if hooks[name][mod_name]['disabled'] < 5:
                try:
                    hooks[name][mod_name]['run'](**kw)
                except:
                    traceback.print_exc()
                    hooks[name][mod_name]['disabled'] += 1
                    if hooks[name][mod_name]['disabled'] == 5:
                        logging.debug('"{0}" was disabled.'.format(mod_name))

