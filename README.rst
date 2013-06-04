======================
Multi-Threaded IRC bot
======================

This is a multi-threaded IRC bot that was designed to connect to
a "feed" network (irc.wikimedia.org) and relay those to the client
network (irc.freenode.net). An example bot would look like::

    #!/usr/bin/env python
    from __future__ import unicode_literals
    import Queue

    from mtirc import bot
    from mtirc import settings

    config = settings.config
    config['nick'] = 'nick'

    class RcvThread(bot.ReceiveThread):
        def parse(self, channel, text, sender):
            print text
            if text.startswith('!ping'):
                self.pull.put((channel, 'pong'))
                self.debug('got a ping')
            elif channel == config['nick']:
                #pm'ing with bot
                if sender.host == 'me@me.com':
                    chan = text.split(' ')[0]
                    real_text = ' '.join(text.split(' ')[1:])
                    self.pull.put((chan, real_text))

    push = Queue.Queue()
    pull = Queue.Queue()
    b = bot.Bot(push, pull, RcvThread, config, use_rc=False)
    b.run()

Features
=========

* Can use as many parse threads as set in config

* Will attempt to reconnect if disconnected

* Reads from a configuration file at ``~/localsettings.py``

* More to come!

License
=========

* Released under the MIT License