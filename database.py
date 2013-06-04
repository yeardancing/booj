import sqlite3
import os, sys
from ID3 import *

class BoojDb():
    def __init__(self, dbName):
        self.dbName = dbName
        self.conn = sqlite3.connect(dbName)
        self.c = conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS songs 
                (id INTEGER NOTNULL,
                 artist VARCHAR(64) NOT NULL,
                 title VARCHAR(64) NOT NULL,
                 album VARCHAR(64) NOT NULL,
                 filename VARCHAR(64) NOT NULL)'
        c.execute(sql)

    def __del__(self):
        self.conn.close()

    def rebuildDatabase(self, musicRoot):
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
                               id3info['GENRE'],
                               id3info['YEAR'],
                               id3info['TRACKNUMBER'])
                    self.c.execute('INSERT INTO songs VALUES(?,?,?,?,?,?,?)', 
                                   newsong)
                    self.conn.commit() 
                    sid = sid + 1

# Do this instead
#t = ('RHAT',)
#c.execute('SELECT * FROM stocks WHERE symbol=?', t)
#print c.fetchone()
#purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
#             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
#             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
#            ]
#c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
#for row in c.execute('SELECT * FROM stocks ORDER BY price'):
