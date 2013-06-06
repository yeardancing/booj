import sqlite3
import os, sys
from ID3 import *

class BoojDb():
    def __init__(self, dbName):
        self.dbName = dbName

    def getArtists(self):
        conn = sqlite3.connect(self.dbName)
        conn.text_factory = str
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT artist FROM songs')
        artists = cur.fetchall()
        conn.close()
        return artists

    def rebuildDatabase(self, musicRoot):
        conn = sqlite3.connect(self.dbName)
        conn.text_factory = str
        cur = conn.cursor()
        sql = "CREATE TABLE IF NOT EXISTS songs\
                (id INTEGER NOT NULL,\
                 artist VARCHAR(64) NOT NULL,\
                 title VARCHAR(64) NOT NULL,\
                 album VARCHAR(64) NOT NULL,\
                 filename VARCHAR(64) NOT NULL)"
        cur.execute(sql)
        sid = 1
        for path, subdirs, files in os.walk(musicRoot):
            for filename in files:
                f = os.path.join(path, filename)
                if str(f).endswith('mp3'):
                    currfile = str(f)
                    try:
                        id3info = ID3(currfile)
                    except InvalidTagError, message:
                        print "Invalid ID3 tag:", message
                        continue

                    newsong = (sid, 
                               id3info['ARTIST'], 
                               id3info['TITLE'],
                               id3info['ALBUM'],
                               #id3info['GENRE'],
                               #id3info['YEAR'],
                               #id3info['TRACKNUMBER'])
                               currfile)
                    cur.execute('INSERT INTO songs VALUES(?,?,?,?,?)', newsong)
                    conn.commit() 
                    sid = sid + 1
        conn.close()

