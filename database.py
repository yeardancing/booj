import sqlite3
import os, sys
from ID3 import *

class BoojDb():
    def __init__(self, dbName):
        self.dbName = dbName

    def getArtists(self):
        conn = sqlite3.connect(self.dbName)
        #conn.text_factory = str
        cur = conn.cursor()
        try:
            cur.execute('SELECT DISTINCT artist, artistId FROM songs')
            artists = cur.fetchall()
        except sqlite3.OperationalError:
            print "Error connecting to database."
            artists = []

        conn.close()
        return artists

    def getArtistById(self, artistId):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT artist FROM songs WHERE artistId=?', [artistId])
        artist = cur.fetchall()
        conn.close()
        if artist and len(artist) == 1:
            return artist[0]
        else:
            return ''

    def getArtistBySongId(self, songId):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT artist FROM songs WHERE id=?', [songId])
        artist = cur.fetchall()
        conn.close()
        if artist and len(artist) == 1:
            return artist[0]
        else:
            return ''
    
    def getSongsByArtistId(self, artistId):
        conn = sqlite3.connect(self.dbName)
        #conn.text_factory = str
        cur = conn.cursor()
        cur.execute('SELECT title, id FROM songs WHERE artistId=?', [artistId])
        songs = cur.fetchall()
        conn.close()
        return songs

    def getSongFileById(self, songId):
        conn = sqlite3.connect(self.dbName)
        #conn.text_factory = str
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT filename FROM songs WHERE id=?', [songId])
        filename = cur.fetchall()
        conn.close()
        if filename and len(filename) == 1:
            return filename[0]
        else:
            return ''

    def getSongTitleBySongId(self, songId):
        conn = sqlite3.connect(self.dbName)
        #conn.text_factory = str
        cur = conn.cursor()
        cur.execute('SELECT DISTINCT title FROM songs WHERE id=?', [songId])
        name = cur.fetchall()
        conn.close()
        if name and len(name) == 1:
            return name[0]
        else:
            return ''

    def validateTags(self, id3info):
        artist = title = album = genre = 'Unknown'
        year = 0
        for k, v in id3info.items():
            if k == 'ARTIST':
                artist = id3info['ARTIST']
            elif k == 'TITLE':
                title = id3info['TITLE']
            elif k == 'ALBUM':
                album = id3info['ALBUM']
            elif k == 'GENRE':
                genre = id3info['GENRE']
            elif k == 'YEAR':
                year = id3info['YEAR']
        return artist, title, album, genre, int(year)

    def rebuildDatabase(self, musicRoot):
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()
        cur.executescript("DROP TABLE IF EXISTS songs;\
                          CREATE TABLE songs\
                          (id INTEGER NOT NULL,\
                          artist TEXT,\
                          artistId INTEGER NOT NULL,\
                          title TEXT,\
                          album TEXT,\
                          genre TEXT,\
                          year INTEGER NOT NULL,\
                          filename TEXT)")
        conn.commit()
        sid = 1
        artistIds = {}
        aid = 1
        for path, subdirs, files in os.walk(musicRoot):
            for filename in files:
                f = os.path.join(path, filename)
                if str(f).endswith('.mp3'):
                    currfile = str(f)
                    try:
                        id3info = ID3(currfile)
                    except InvalidTagError, message:
                        print "Invalid ID3 tag:", message
                        continue

                    artist, title, album, genre, year = self.validateTags(id3info)
                    if artist in artistIds:
                        artistId = artistIds[artist]
                    else:
                        artistId = aid
                        artistIds[artist] = aid
                        aid += 1

                    try:
                        cur.execute('INSERT INTO songs VALUES(?,?,?,?,?,?,?,?)',
                                    (sid, 
                                    unicode(artist, 'latin_1'), 
                                    artistId,
                                    unicode(title, 'latin_1'),
                                    unicode(album, 'latin_1'),
                                    unicode(genre, 'latin_1'),
                                    year,
                                    unicode(currfile, 'latin_1')))
                        conn.commit() 
                        sid = sid + 1
                    except KeyError:
                        print 'Woah, bad tags!'
                        for k, v in id3info.items():
                            print k, ":", v
        conn.close()

