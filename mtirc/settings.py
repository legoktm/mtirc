import os
import sys

import pinger

config = {

    # Connection info
    'connections': {'card.freenode.net': {'channels': [
                                                       ],
                                          },
                    },
    'port': 6667,  # For all networks
    'default_network': 'card.freenode.net',
    'default_channel': '##',  # On default_network

    # Identification info
    'nick': 'Forgot_to_set_nick',  # Both networks
    'name': 'mtirc',  # Both networks

    # How many processing threads to start
    'threads': 5,

    # Cache file
    'cache_file': 'cache',

    # Whether to use memcache if possible
    'use_memcache': True,
    'mc_host': '127.0.0.1',

    # How many seconds to wait in between reconnection attempts
    'reconnection_interval': 5,

    # NickServ information
    'authenticate': False,
    'ns_username': '',
    'ns_pw': '',

    # Whether to send debug information to the channel
    'debug': True,

    # Memory allocations for grid engine
    'memory': {},

    # How many seconds to wait in between messages
    'delay_time': 1,

    # Allow for modules to be stored and run on hits.
    # Modules should take **kwargs for best performance
    'modules': {'pinger': pinger.run,
                },

    # After how many exceptions should modules be disabled
    # If None, never disable modules
    'disable_on_errors': 5,

}

# Change config via commandline
# TODO: Use ArgParse or something
if '--debug' in sys.argv:
    config['debug'] = True
if '--file-cache' in sys.argv:
    config['use_memcache'] = False
if '--memcache' in sys.argv:
    config['use_memcache'] = True

if __name__ == '__main__':
    import simplejson as json
    print json.dumps(config, sort_keys=True, indent=4 * ' ')

