import os, sys, Queue, time
import threading
from booj.models import model
from booj.lib.player import BoojPlayer
import gobject
gobject.threads_init()
import pygst
pygst.require ("0.10")
import gst

runLoop = True
q = Queue.Queue()

class MainLooper(threading.Thread):
    def onMsg(pl, msg):
        if msg.type == gst.MESSAGE_ERROR:
            error, debug = msg.parse_error()
            print error, debug

    def run(self):
        global runLoop
        global q
        self.mainloop = gobject.MainLoop()
        self.pl = gst.element_factory_make("playbin", "player")
        context = self.mainloop.get_context()
        #bus = pl.get_bus()

        time = 0.0
        while True:
            try:
                c = ''
                print 'listening...'
                try:
                    c = q.get(True, 2.0)
                    print 'got a... ', c[0]
                except Queue.Empty:
                    print 'nothing...'
                    continue

                if c[0] in 'sqdp0152ngl':
                    if c[0] == 's':
                        pl.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT, 230 * gst.SECOND) 
                    elif c[0] == 'q':
                        pl.set_state(gst.STATE_NULL)
                        print 'bye!'
                        return 
                    elif c[0] == 'd':
                        try: 
                            duration, format = pl.query_duration(gst.FORMAT_TIME)
                            print 'Duration', duration / gst.SECOND
                        except:
                            raise GenericException("Couldn't fetch song duration")
                    elif c[0] == 'p':
                        try:
                            position, format = pl.query_position(gst.FORMAT_TIME)
                            print 'position', float(position) / gst.SECOND
                        except:
                            raise GenericException("Couldn't fetch song position")
                    elif c[0] == '0':
                        try:
                            pl.set_property('volume', 0.0)
                        except:
                            raise GenericException("couldn't set volume")
                    elif c[0] == '1':
                        try:
                            pl.set_property('volume', 1.0)
                        except:
                            raise GenericException("couldn't set volume")
                    elif c[0] == '5':
                        try:
                            pl.set_property('volume', 0.5)
                        except:
                            raise GenericException("couldn't set volume")
                    elif c[0] == '2':
                        try:
                            pl.set_property('volume', 0.2)
                        except:
                            raise GenericException("couldn't set volume")
                    elif c[0] == 'n':
                        pl.set_state(gst.STATE_PAUSED)
                    elif c[0] == 'g':
                        pl.set_state(gst.STATE_PLAYING)
                    elif c[0] == 'l':
                        pl.set_state(gst.STATE_NULL)
                        pl.set_property('uri','file://'+os.path.abspath('/home/dspadaro/wonderful.mp3'))
                        pl.set_state(gst.STATE_PLAYING)
                    
            except IOError: 
                print 'IOerror...'

            q.task_done()
            if not runLoop:
                return

class GstreamerPlayer(BoojPlayer):
    def __init__(self):
        MainLooper().start()
        global q
        self.queue = q

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        global runLoop
        print 'exiting Gstreamer player...'
        runLoop = False

    def set_location(self, location):
        """
        Queue up a song to play next.  This takes a string
        of the absolute path to the resource.

        Be careful! If your let your song run to completion
        you will no longer have a location set.  The files
        you load are "clear on complete"

        Returns the length of the song in seconds as a float.

        """
        totalTime = 0.0
        self.pl.set_state(gst.STATE_NULL)
        self.pl.set_property('uri', 'file://'+os.path.abspath(location))
        self.pl.set_state(gst.STATE_PLAYING)
        self.imPlaying = True
        try:
            duration, format = self.pl.query_duration(gst.FORMAT_TIME)
            totalTime = duration / gst.SECOND
        except Exception:
            print "whoops, something didn't query.."
        return totalTime

    def query_position(self):
        """Returns a Position object with the following members:
            * the current position as a float that is
              the percentage of the way through the song.
            * the current time in seconds
            * the song length in seconds
        """
        pos = model.Position()
        position, format = self.pl.query_position(gst.FORMAT_TIME)
        pos.currentTime = float(position) / gst.SECOND
        return pos

    def seek(self, position):
        """Jump to the specified position.
        Position is specified by a percentage (float) value.
        """
        q.put('s')
        seekTime = position * self.query_position().currentTime * gst.SECOND
        self.pl.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_KEY_UNIT, seekTime) 

    def pause(self):
        """Pauses current song in progress.  Does nothing if
        no song is playing.
        """
        self.stop()

    def unpause(self):
        """Unpauses current song in progress.  Does nothing if
        no song is loaded.
        """
        self.play()

    def play(self):
        """Play your song.
        A file location must have been specified first.
        But note that you must also call play; songs do 
        not automagically start playing on load.

        """
        self.pl.set_state(gst.STATE_PLAYING)
        self.imPlaying = True

    def stop(self):
        """Pauses current song in progress.  Same as pause.
        """
        self.pl.set_state(gst.STATE_PAUSED)
        self.imPlaying = False

    def is_playing(self):
        """Returns True if a song is currently playing,
        false otherwise.
        """
        return self.imPlaying

    def get_volume(self):
        """Returns analog volume as an integer percentage, 0-100.
        """
        return self.pl.get_property('volume') * 100

    def set_volume(self, vol):
        """This function sets the analog volume using
        the ALSA soundcard driver. Vol is an integer
        percentage, 0-100.

        """
        self.pl.set_property('volume', float(vol) / 100.0)

