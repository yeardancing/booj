#!/usr/bin/env python

import operator, os, sys

import cherrypy
from booj.lib import template, player
from booj import database

default_server_ip = "192.168.1.5"
server_ip = default_server_ip

class Root(object):

    def __init__(self, db, player):
        self.db = db
        self.myplayer = player

    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        artists = self.db.getArtists()
        return template.render(artists=artists)

    @cherrypy.expose
    @template.output('artist.html')
    def artist(self, id):
        songs = self.db.getSongs(id)
        return template.render(songs=songs)

    @cherrypy.expose
    @template.output('song.html')
    def song(self, id):
        dummyfile = 'file:/home/dspadaro/src/python/cherrypy/Sine_wave_440.ogg'
        if cherrypy.request.method == 'POST':
            if self.myplayer.is_playing():
                self.myplayer.stop()
            else:
                self.myplayer.set_location(dummyfile) 
                self.myplayer.play()

        return template.render(id=id)

def main(db):
    mydb = database.BoojDb(db)
    myplayer = player.BoojPlayer(name="boojPlayer")

    def _save_data():
        if myplayer.is_playing():
            myplayer.stop()
        myplayer.destroy()
        #databaseobj = open(database, 'wb')

    if hasattr(cherrypy.engine, 'subscribe'):
        cherrypy.engine.subscribe('stop', _save_data)
    else:
        cherrpy.engine.on_stop_engine_list.append(_save_data)
        
    #This could go in a global confi gfile
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
        'server.socket_host': server_ip
    })

    myplayer.start()
    cherrypy.quickstart(Root(mydb, myplayer), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

if __name__ == '__main__':
    if len(sys.argv) == 3:
        server_ip =  sys.argv[2]
    main(sys.argv[1])

