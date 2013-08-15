#!/usr/bin/env python

import sys, time
from booj.lib import player

def main(srcfile):
    myplayer = player.BoojPlayer()
    myplayer.set_location(srcfile)
    print "main sleeping.."
    myplayer.play()
    time.sleep(4)
    playing = myplayer.is_playing()
    print "playing ? : %s" % playing
    time.sleep(3)
    myplayer.stop()
    print "main done"

if __name__ == '__main__':
    main(sys.argv[1])

