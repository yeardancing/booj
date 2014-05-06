#!/usr/bin/env python

import sys, time
from booj.lib import player

def main(srcfile):
    myplayer = player.BoojPlayer()
    duration = myplayer.set_location(srcfile)
    if duration != 194.27:
        print 'playerTest:' + '\033[91m' + '\t\tFAIL' + '\033[0m'
        return
    myplayer.play()
    time.sleep(2)
    playing = myplayer.is_playing()
    #print "playing ? : %s" % playing
    time.sleep(2)
    myplayer.stop()
    #print "main done"
    print 'playerTest:' + '\033[92m' + '\t\tPASS' + '\033[0m'

if __name__ == '__main__':
    main(sys.argv[1])

