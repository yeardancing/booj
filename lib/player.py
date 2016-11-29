import Queue
import time
from booj.models import model
from simpistreamer.pipystreamer import PiPyStreamer

class BoojPlayer:
    def __init__(self):
        self.q = Queue.Queue()
        self.resp_q = Queue.Queue()
        self.server = PiPyStreamer(self.q, self.resp_q).start()

    def set_location(self, location):
        """
        Queue up a song to play next.  This takes a string
        of the absolute path to the resource.

        Be careful! If your let your song run to completion
        you will no longer have a location set.  The files
        you load are "clear on complete"

        Returns the length of the song in seconds as a float.

        """
        uri = 'l ' + location
        self.q.put(uri)

        time.sleep(0.3)
        length = 0.0
        self.q.put('d')
        try:
            length = float(self.resp_q.get())
        except ValueError:
            print "couldn't get duration after load"
        return length

    def query_position(self):
        """Returns a Position object with the following members:
            * the current position as a float that is
              the percentage of the way through the song.
            * the current time in seconds
            * the song length in seconds
        """
        pos = model.Position()

        self.q.put('p')
        curr = self.resp_q.get()
        try:
            pos.currentTime = float(curr)
        except ValueError:
            print "couldn't query position:" + curr

        self.q.put('d')
        length = self.resp_q.get()
        try:
            pos.maxTime = float(length)
        except ValueError:
            print "couldn't query position:" + length
        if pos.maxTime != 0:
            pos.currentPosition = pos.currentTime / pos.maxTime 
        else:
            pos.currentPosition = 0
        return pos

    def seek(self, position):
        """Jump to the specified position.
        Position is specified by a percentage (float) value.
        """
        self.q.put('d')
        try:
            length = float(self.resp_q.get())
        except ValueError:
            print "couldn't seek (bad duration)"
        seek = 's ' + str(position * length)
        self.q.put(seek)

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
        self.q.put('g')

    def stop(self):
        """Pauses current song in progress.  Same as pause.
        """
        self.q.put('n')

    def is_playing(self):
        """Returns True if a song is currently playing,
        false otherwise.
        """
        return False

    def get_volume(self):
        """Returns analog volume as an integer percentage, 0-100.
        """
        volume = -1.0
        self.q.put('t')
        vol = self.resp_q.get()
        try:
            volume = 100 * float(vol)
        except ValueError:
            print "Couldn't get volume" + vol
        return volume

    def set_volume(self, vol):
        """This function sets the analog volume using
        the ALSA soundcard driver. Vol is an integer
        percentage, 0-100.

        """
        self.q.put('v ' + str(vol))

    def destroy(self):
        """Stops the music server.

        """
        self.q.put('q')


