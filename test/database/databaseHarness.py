#!/usr/bin/env python

import os, sys
from booj import database

def testGetArtistById(db):
    myartist = db.getArtistById(11)
    if myartist[0] == 'New Order':
        return True
    else:
        return False

def testGetSongFileById(db):
    myfile = db.getSongFileById(12)
    if myfile[0] == '/home/dspadaro/Music/Amazon MP3/Department Of Eagles/In Ear Park/05 - Around The Bay.mp3':
        return True
    else:
        return False

def main():
    mydb = database.BoojDb('booj/test/database/test.db')

    if testGetSongFileById(mydb):
        print 'getSongFileById:' + '\033[92m' + '\tPASS' + '\033[0m'
    else:
        print 'getSongFileById:' + '\033[91m' + '\tFAIL' + '\033[0m'

    if testGetArtistById(mydb):
        print 'getArtistById:' + '\033[92m' + '\t\tPASS' + '\033[0m'
    else:
        print 'getArtistById:' + '\033[91m' + '\t\tFAIL' + '\033[0m'


if __name__ == '__main__':
    main()

