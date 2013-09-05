#!/usr/bin/env python

import operator, os, sys, socket

import cherrypy
from booj.lib import template, player
from booj import database

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip

server_ip = get_lan_ip()


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
    def artist(self, artistId):
        songs = self.db.getSongsByArtistId(artistId)
        myartist = self.db.getArtistById(artistId)
        return template.render(artist=myartist, songs=songs)

    @cherrypy.expose
    @template.output('song.html')
    def song(self, songId):
        songfile = self.db.getSongFileById(songId)
        if cherrypy.request.method == 'POST':
            if self.myplayer.is_playing():
                self.myplayer.stop()
            else:
                print "playing", songfile[0]
                self.myplayer.set_location(songfile[0]) 
                self.myplayer.play()

        return template.render(songId=songId)

def main(db):
    mydb = database.BoojDb(db)
    myplayer = player.BoojPlayer()

    def _save_data():
        if myplayer.is_playing():
            myplayer.stop()
        #databaseobj = open(database, 'wb')

    if hasattr(cherrypy.engine, 'subscribe'):
        cherrypy.engine.subscribe('stop', _save_data)
    else:
        cherrpy.engine.on_stop_engine_list.append(_save_data)
        
    #This could go in a global config file
    cherrypy.config.update({
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
        'server.socket_host': server_ip
    })

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

