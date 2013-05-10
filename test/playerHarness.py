#!/usr/bin/env python

import sys, time
from booj.lib import player

def main(srcfile):
    myplayer = player.BoojPlayer(name = "boojPlayer")
    myplayer.start()
    print "main sleeping.."
    time.sleep(10)
    myplayer.destroy()
    print "main done"

if __name__ == '__main__':
    main(sys.argv[1])

