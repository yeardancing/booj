#!/usr/bin/env python

import operator, os, sys

import cherrypy
from booj.lib import template

default_server_ip = "192.168.1.6"
server_ip = default_server_ip

class Root(object):

    def __init__(self, data):
        self.data = data

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
        return template.render()

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

    def _save_data():
        databaseobj = open(database, 'wb')

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

    cherrypy.quickstart(Root(data), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

if __name__ == '__main__':
    if len(sys.argv) == 3:
        server_ip =  sys.argv[2]
    main(sys.argv[1])

