#!/usr/bin/python3
# -*- coding:utf-8 -*-

###############################################################################
# Sample Python script which run as a service (daemon).
#
# Usage:
#       myservice.py start|stop|restart
#
###############################################################################

import os
import sys
import time
import argparse
from   mydaemon import Daemon

# Daemon name. It's only used in messages.
DAEMON_NAME = 'My Service'
# Cleanstop wait time before to kill the process.
DAEMON_STOP_TIMEOUT = 10
# Daemon pid file.
PIDFILE = '/tmp/myservice.pid'
# Deamon run file. "stop" request deletes this file to inform the process and
# waits DAEMON_STOP_TIMEOUT seconds before to send SIGTERM. The process has a
# change to stop cleanly if it's written appropriately.
RUNFILE = '/tmp/myservice.run'
# Sleep time.
LOOP_SLEEP = 2
# Debug mode.
DEBUG = 0



# -----------------------------------------------------------------------------
def get_args():
    '''
    >>> get_args()
    ('start',)
    >>> get_args()
    ('stop',)
    '''

    try:
        parser =  argparse.ArgumentParser()
        parser.add_argument('action', help='action',
                            choices=['start', 'stop', 'restart'])
        args = parser.parse_args()

        result = (args.action, )
    except Exception as err:
        if DEBUG:
            raise
        else:
            sys.stderr.write('%s\n' % (err))

        result = (None, )

    return result



# -----------------------------------------------------------------------------
def wait(timeout=60):
    '''
    >>> wait(20)
    True
    >>> wait(None)
    False
    '''
    try:
        # Wait [timeout] seconds while there is no stop request.
        t0 = time.time()
        while os.path.exists(RUNFILE) and ((time.time()-t0) < timeout):
            time.sleep(1.0)

        result = True
    except Exception as err:
        if DEBUG:
            raise
        else:
            sys.stderr.write('%s\n' % (err))

        result = False

    return result



# -----------------------------------------------------------------------------
class MyDaemon(Daemon):
    def run(self):
        '''
        Daemon start to run here.
        '''

        # Run while there is no stop request.
        while os.path.exists(RUNFILE):
            try:
                pass
            except Exception as err:
                if DEBUG:
                    raise
                else:
                    sys.stderr.write('%s\n' % (err))
            finally:
                wait(timeout=LOOP_SLEEP)



# -----------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        # Get arguments.
        (action, ) = get_args()

        # Create daemon object.
        d = MyDaemon(name=DAEMON_NAME, pidfile=PIDFILE, runfile=RUNFILE,
                     stoptimeout=DAEMON_STOP_TIMEOUT, debug=DEBUG)

        # Action requested.
        if action == 'start':
            d.start()
        elif action == 'stop':
            d.stop()
        elif action == 'restart':
            d.restart()
        else:
            raise NameError('Unknown action')

        sys.exit(0)
    except Exception as err:
        if DEBUG:
            raise
        else:
            sys.stderr.write('%s\n' % err)

        sys.exit(1)
