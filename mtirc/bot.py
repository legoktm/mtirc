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

import irc.client as irclib
import re
import threading
import time
import traceback
import Queue

import cache

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


class ReceiveThread(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.bot = bot
        self.queue = bot.push
        self.pull = bot.pull
        self.config = bot.config

    def parse(self, channel, text, sender, server):
        #This should be sub-classed
        for name in self.bot.config['modules']:
            try:
                cont = self.bot.config['modules'][name](channel=channel,
                                                        text=text,
                                                        sender=sender,
                                                        server=server,
                                                        bot=self.bot,
                                                        )
                if not cont:
                    break
            except:
                traceback.print_exc()
                #now we need to track how many times its died
                if self.config['disable_on_errors']:
                    if name in self.bot.cache['errors']:
                        count = self.bot.cache['errors'][name]
                        count += 1
                        if count >= self.config['disable_on_errors']:
                            del self.bot.config['modules'][name]
                            self.debug('The {0} module was disabled due to {1} errors.'.format(
                                name, count
                            ))
                        else:
                            self.bot.cache['errors'][name] = count
                    else:
                        self.bot.cache['errors'][name] = 1


    def debug(self, msg):
        if self.config['debug']:
            msg = unicode(msg)
            self.msg(None, u'DEBUG: ' + msg)

    def msg(self, channel, text):
        #place holder for logging
        self.pull.put(channel, text)

    def run(self):
        while True:
            channel, text, sender, server = self.queue.get()
            try:
                self.parse(channel, text, sender, server)
            except:
                traceback.print_exc()
            self.queue.task_done()


class Bot:
    def __init__(self, config):
        self.irc = irclib.IRC()
        self.push = Queue.Queue()  # Queue for incoming messages
        self.pull = Queue.Queue()  # Queue for outgoing messages
        self.delay = 0  # When the last message was sent to the server
        self.config = config
        self.delayTime = self.config['delay_time']
        self.cache = cache.Cache(self.config)
        self.init_cache()

    def init_cache(self):
        self.cache['errors'] = {}

    def on_msg(self, c, e):
        #print e.type
        #print e.arguments
        #print e.source
        #print e.target
        self.msg(e.target, e.arguments[0], e.source, c.server)

    def msg(self, channel, text, sender, server):
        #this is mainly a placeholder for other things
        self.push.put((channel, text, sender, server))

    def queue_msg(self, channel, text):
        self.pull.put((channel, text))

    def send_msg(self, channel, text):
        try:
            self._send_msg(channel, text)
        except:
            traceback.print_exc()

    def _send_msg(self, channel, text):
        if not channel:
            channel = self.config['default_channel']
        d = time.time()
        if d - self.delay < self.delayTime:
            time.sleep(self.delayTime - (d - self.delay))
        self.delay = d
        if not isinstance(text, basestring):
            text = unicode(text)
        self.servers[self.config['default_network']].privmsg(channel, text)

    def get_version(self):
        # This should be improved
        return "mtirc v0.2.1"

    def on_ctcp(self, c, e):
        """Default handler for ctcp events.

        Replies to VERSION and PING requests and relays DCC requests
        to the on_dccchat method.
        """
        nick = e.source.nick
        if e.arguments[0] == "VERSION":
            c.ctcp_reply(nick, "VERSION " + self.get_version())
        elif e.arguments[0] == "PING":
            if len(e.arguments) > 1:
                c.ctcp_reply(nick, "PING " + e.arguments[1])

    def on_disconnect(self, c, e):
        self.connect_to_server(c.server)

    def auth(self):
        self.send_msg('nickserv', 'identify {0} {1}'.format(self.config['ns_username'], self.config['ns_pw']))

    def connect_to_server(self, server):
        d = self.config['connections'][server]
        self.servers[server] = self.irc.server()
        self.servers[server].connect(server,
                                     d.get('port', self.config['port']),
                                     d.get('nick', self.config['nick']),
                                     d.get('name', self.config['name']),
                                     )
        if d.get('authenticate', self.config['authenticate']):
            self.auth()
        if 'channels' in d:
            for channel in d['channels']:
                self.servers[server].join(channel)

    def run(self):
        for i in range(0, self.config['threads']):
            t = ReceiveThread(self)
            t.setDaemon(True)
            t.start()

        self.irc.add_global_handler('privmsg', self.on_msg)
        self.irc.add_global_handler('pubmsg', self.on_msg)
        self.irc.add_global_handler('ctcp', self.on_ctcp)
        self.irc.add_global_handler('disconnect', self.on_disconnect)

        self.servers = {}
        for server in self.config['connections']:
            self.connect_to_server(server)

        while True:
            self.irc.process_once(timeout=0.1)
            try:
                channel, text = self.pull.get(block=False)
                self.send_msg(channel, text)
            except Queue.Empty:
                pass

