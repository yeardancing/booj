from datetime import datetime

class Song(object):

    def __init__(self, title, artist, ident):
        self.title = title
        self.artist = artist
        self.id = ident

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.title)


class Artist(object):
   
   def __init__(self, name):
    self.name = name
    self.id = hex(hash(tuple([name])))[2:]

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.name)

class PlayList(object):
   def __init__(self, name):
    self.name = name
    self.time = datetime
    self.id = hex(hash(tuple([name])))[2:]

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.name)

    def add_song(self, song, artist):
        song = Song(artist, song)
        self.songs.append(song)
        return song
