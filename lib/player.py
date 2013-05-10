
import sys, os, time, thread, threading
import glib, gobject
#import pygst
#pygst.require('0.10')
import gst
#import gst.interfaces

class BoojPlayer(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.running = False
        self.player = gst.element_factory_make("playbin2", "player")
        fakesink = gst.element_factory_make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        self.on_eos = False

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def run(self):
        self.running = True
        loop = gobject.MainLoop()
        gobject.threads_init()
        #context = loop.get_context()
        while 1:
            #handle commands here
            print "in a loop"
            time.sleep(2)
            if self.running == False:
                break
            #context.iteration(True)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.playmode = False
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.playmode = False
    
    def set_location(self, location):
        self.player.set_property('uri', location)

    def query_position(self):
        "Returns a (position, duration) tuple"
        try:
            position, format = self.player.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self.player.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE

        return (position, duration)

    def seek(self, duration):
        """
        @param location: time to seek to, in nanoseconds
        """
        gst.debug("seeking to %r" % location)
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
                gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                gst.SEEK_TYPE_SET, location,
                gst.SEEK_TYPE_NONE, 0)

        res = self.player.send_event(event)
        if res:
            gst.info("setting new stream time to 0")
            self.player.set_new_stream_time(0L)
        else:
            gst.error("Seek to %r failed" % location)

    def pause(self):
        gst.info("pausing player")
        self.player.set_state(gst.STATE_PAUSED)
        self.playmode = False

    def play(self):
        gst.info("playing player")
        self.player.set_state(gst.STATE_PLAYING)
        self.playmode = True

    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        gst.info("stopped player")

    def get_state(self, timeout=1):
        return self.player.get_state(timeout=timeout)

    def is_playing(self):
        return self.playing

    def destroy(self):
        self.running = False


