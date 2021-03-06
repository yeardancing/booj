#!/usr/bin/env python

import sys, time
from booj.models import model
from booj.lib import player

def main(srcfile):
    myplayer = player.BoojPlayer()
    duration = myplayer.set_location(srcfile)
    if duration !=  211.43510204:
        print 'expected duration  211.43510204, got', duration
        print 'playerTest:' + '\033[91m' + '\t\tFAIL' + '\033[0m'
    myplayer.play()
    time.sleep(2)
    playing = myplayer.is_playing()
    time.sleep(2)
    position = model.Position()
    position = myplayer.query_position()
    print position
    myplayer.stop()
    print 'playerTest:' + '\033[92m' + '\t\tPASS' + '\033[0m'
    myplayer.destroy()

if __name__ == '__main__':
    main(sys.argv[1])

