#!/usr/bin/env python

import operator, os, sys

import cherrypy
from booj.lib import template, player

server_ip = "192.168.1.6"

class Root(object):

    def __init__(self, data, player):
        self.data = data
        self.myplayer = player

    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        artists = self.data[0]
        return template.render(artists=artists)

    @cherrypy.expose
    @template.output('artist.html')
    def artist(self, id):
        songs = self.data[1]
        return template.render(songs=songs)

    @cherrypy.expose
    @template.output('song.html')
    def song(self, id):
        dummyfile = 'file:/home/dspadaro/src/python/cherrypy/half_a_person.ogg'
        if cherrypy.request.method == 'POST':
            if self.myplayer.is_playing():
                self.myplayer.stop()
            else:
                self.myplayer.set_location(dummyfile) 
                self.myplayer.start()
                self.myplayer.play()

        return template.render(id=id)

def main(database):
    # do database opening and parsing stuff here
    #if os.path.exists(database):
        # ...
    #else:
    artists = ["The Celltones", 
                "Devo", 
                "Fleet Foxes", 
                "Eric Clapton",
                "James Brown"]
    songs = ["Before You Accuse Me", 
            "Hey Hey Hey", 
            "Walking Blues", 
            "Malted Milk", 
            "Signe",
            "Tears in Heaven"]
    data = [artists, songs]
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

    cherrypy.quickstart(Root(data, myplayer), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

if __name__ == '__main__':
    main(sys.argv[1])

