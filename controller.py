#!/usr/bin/env python

import operator, os, sys

import cherrypy
from booj.lib import template

server_ip = "172.22.76.122"

class Root(object):

    def __init__(self, data):
        self.data = data

    @cherrypy.expose
    @template.output('index.html')
    def index(self):
        artists = self.data
        return template.render(artists=artists)

def main(database):
    # do database opening and parsing stuff here
    #if os.path.exists(database):
        # ...
    #else:
    """
    <a href="#">A Tribe Called Quest</a></li>
    <a href="#">Guttermouth</a></li>
    <a href="#">Iggy Popp</a></li>
    <a href="#">Led Zeppelin</a></li>
    <a href="#">Moby</a></li>
    <a href="#">Primus</a></li>
    <a href="#">Rancid</a></li>
    <a href="#">Ricky Martin</a></li>
    <a href="#">Boy Sets Fire</a></li>
    <a href="#">Save Ferris</a></li>
    <a href="#">Noby</a></li>
    <a href="#">Limus</a></li>
    <a href="#">Aancid</a></li>
    <a href="#">Ticky Martin</a></li>
    <a href="#">Woy Sets Fire</a></li>
    <a href="#">Wave Ferris</a></li>
    """
    artists = {"The Celltones", "Devo", "Fleet Foxes", "Eric Clapton", "James Brown"}

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

    cherrypy.quickstart(Root(artists), '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

if __name__ == '__main__':
    main(sys.argv[1])

