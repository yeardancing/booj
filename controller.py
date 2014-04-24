#!/usr/bin/env python

import operator, os, sys, socket, getopt
import cherrypy
import json
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


class Root(object):

    def __init__(self, db, player):
        self.db = db
        self.myplayer = player

    @cherrypy.expose
    @template.output('index.html')
    def index(self, playnow=None):
        artists = self.db.getArtists()
        if cherrypy.request.method == 'POST':
            cherrypy.response.headers['Content-Type'] = "application/json"
            if playnow:
                message = self.actOnPlayNow(playnow)
            return json.dumps(message)
        return template.render(artists = artists,
                               isPlaying = self.myplayer.is_playing())

    @cherrypy.expose
    @template.output('artist.html')
    def artist(self, artistId, playnow=None):
        songs = self.db.getSongsByArtistId(artistId)
        myartist = self.db.getArtistById(artistId)
        if cherrypy.request.method == 'POST':
            cherrypy.response.headers['Content-Type'] = "application/json"
            if playnow:
                message = self.actOnPlayNow(playnow)
            return json.dumps(message)
        return template.render(artist = myartist, 
                               songs = songs,
                               isPlaying = self.myplayer.is_playing())

    @cherrypy.expose
    @template.output('song.html')
    def song(self, songId, playnow=None):
        songfile = self.db.getSongFileById(songId)
        artist = self.db.getArtistBySongId(songId)
        songTitle = self.db.getSongTitleBySongId(songId)
        if cherrypy.request.method == 'POST':
            cherrypy.response.headers['Content-Type'] = "application/json"
            if playnow:
                message = self.actOnPlayNow(playnow)
            else:
                duration = self.myplayer.set_location(songfile[0]) 
                self.myplayer.play()
                message = { 'playing'   : 'true',
                            'artist'    : artist,
                            'song'      : songTitle,
                            'duration'  : int(duration) }
            return json.dumps(message)
        return template.render(songId = songId, 
                               artist = artist, 
                               songTitle = songTitle,
                               isPlaying = self.myplayer.is_playing())

    def actOnPlayNow(self, playnow):
        if str(playnow) == 'true':
            self.myplayer.play() 
            message = { 'playing'  : 'true',
                        'position' : self.myplayer.query_position() }
        else:
            self.myplayer.stop()
            message = { 'playing'  : 'false',
                        'position' : self.myplayer.query_position() }
        return message
    

def main(db, doRebuild):
    mydb = database.BoojDb(db)
    myplayer = player.BoojPlayer()

    if doRebuild:
        mydb.rebuildDatabase(doRebuild)

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
        'tools.encode.on': True, 
        'tools.encode.encoding': 'utf-8',
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
    doRebuild=""
    server_ip = get_lan_ip()
    db="booj.db"
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   "hd:r:a:",
                                   ["database=","rebuild=","address="])
    except getopt.GetoptError:
        print '%s -d <db_file> -r <db_dir> -a <bind_addr>' % sys.argv[0]
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print '%s -d <db_file> -r <db_dir> -a <bind_addr>' % sys.argv[0]
            sys.exit()
        elif opt in ("-d", "--database"):
            db = arg
        elif opt in ("-r", "--rebuild"):
            doRebuild = arg
        elif opt in ("-a", "--address"):
            server_ip = arg
    main(db, doRebuild)

