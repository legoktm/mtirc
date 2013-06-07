======================
Multi-Threaded IRC bot
======================

This is a multi-threaded IRC bot that was designed to connect to
multiple networks load individual modules.
An example bot would look like::

    #!/usr/bin/env python
    from __future__ import unicode_literals

    from mtirc import bot
    from mtirc import ettings

    config = settings.config
    config['nick'] = 'nick'

    def thing(**kw):
        if kw['text'].startswith('!whoami'):
            kw['bot'].queue_msg(kw['channel'], 'You are {0} with the host {1}.'.format(
                kw['sender'].nick, kw['sender'].host))
        return True

    config['modules']['whoami'] = thing

    b = bot.Bot(config)
    b.run()

Features
=========
* Nearly every thing is configurable

* Settings can be set for an individual connection or globally

* Can use as many parse threads as set in config

* Will attempt to reconnect if disconnected

* Will disable modules after too many exceptions

* More to come!

License
=========

* Released under the MIT License