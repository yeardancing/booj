import os, time, threading
import telnetlib
from booj.lib import BoojPlayer

class Mpg123Player(BoojPlayer):
    def __init__(self):
        self.songInfoLock = threading.RLock()
        self.readWriteLock = threading.RLock()
        with self.readWriteLock:
            self.player = telnetlib.Telnet("localhost", "mpg321", 60)
            output = self.player.read_until("\n", 1)
        if not output: #TODO: exception?
            print "Failed to start player!"
            return
        self.set_volume(100)
        with self.songInfoLock:
            self.curr_pos = 0
            self.curr_time = 0
            self.playing = False
            self.location = ''
        self.max_pos = 0
        self.total_time = 0

    def set_location(self, location):
        """
        Queue up a song to play next.  This takes a string
        of the absolute path to the resource.

        Be careful! If your let your song run to completion
        you will no longer have a location set.  The files
        you load are "clear on complete"

        Returns the length of the song in seconds as a float.

        """
        try:
            mylocation = location.encode('ascii', 'ignore')
        except UnicodeDecodeError:
            mylocation = location[0].encode('utf8')
        with self.readWriteLock:
            self.player.write("L " + mylocation + "\n")
            #check for error here..

            # Putting the read_until _before_ the pause causes the song
            # to play 1-2 seconds before pausing, but otherwise we can
            # miss the information in the '@F n ....' lines
            # Perhaps just delay gathering this information until the 
            # song is started (unpaused)?
            #
            #Also should check and see if its necessary to set volume to 0 here
            load_output = self.player.read_until("@F 0\n", 1)
            self.player.write("P\n")
            if not load_output: #TODO: exception?
                print "Failed to load", mylocation
                return
            self.player.write("J 0\n")
            jump_output = self.player.read_until("@J 0\n", 1)
        if not load_output: #TODO: exception?
            print "Failed to load", mylocation
            return
        with self.songInfoLock:
            self.max_pos = self.parse_for_last_frame(load_output)
            self.total_time = self.parse_for_total_time(load_output)
            print "load_output", load_output
            print "jump_output", jump_output
            print "max_pos", self.max_pos
            print "total_time", self.total_time
            self.curr_pos = 0
            self.curr_time = 0;
            self.location = mylocation
        return self.total_time

    def query_position(self):
        """Returns a Position object with the following members:
            * the current position as a float that is
              the percentage of the way through the song.
            * the current time in seconds
            * the song length in seconds
        """
        p = Position()
        with self.songInfoLock:
            curr_pos = self.curr_pos
            p.currentTime = self.curr_time
            p.maxTime = self.total_time
        print 'curr_pos', curr_pos, 'max_pos', self.max_pos
        if curr_pos != 0 and self.max_pos != 0:
            p.currentPosition = (float(curr_pos) / float(self.max_pos))
        else:
            print 'zeroooooooossss!'
        return p 

    def seek(self, position):
        """Jump to the specified position.
        Position is specified by a percentage (float) value.
        """
        with self.songInfoLock:
            location = self.location
        if not location:
            print "seek: No File loaded!"
            return 
        framejump = int(self.max_pos * position)
        with self.readWriteLock:
            self.player.write("J %i\n" % framejump)
            jump_output = self.player.read_until("@J 0\n", 1)
        if not jump_output: # TODO: exception?
            print "Seek failed"

    def pause(self):
        with self.songInfoLock:
            self.playing = False
        with self.readWriteLock:
            self.player.write("P\n")
            self.player.read_until("@P 1\n", 1)

    def unpause(self):
        with self.songInfoLock:
            location = self.location
        if not location:
            print "seek: No File loaded!"
            return 
        with self.readWriteLock:
            self.player.write("P\n")
            output = self.player.read_until("@P 2\n", 1)
        if not output:
            print "Failed to start playing", self.location
            return
        with self.songInfoLock:
            self.playing = True 
        maintenanceEvent = threading.Timer(0.5, self.playerMaintenanceEvent)
        maintenanceEvent.start()

    def play(self):
        """Play your song.
        A file location must have been specified first.
        But note that you must also call play; songs do 
        not automagically start playing on load.

        """
        self.unpause()

    def stop(self):
        self.pause()

    def is_playing(self):
        with self.songInfoLock:
            playing = self.playing
        return playing

    def get_volume(self):
        return self.volume

    def set_volume(self, vol):
        """This function sets the analog volume using
        the ALSA soundcard driver. Vol is an integer
        percentage, 0-100.

        """
        self.volume = vol
        volume_cmd = "amixer sset PCM,0 %d%%" % (self.volume)
        os.system(volume_cmd)

    def parse_for_last_frame(self, output):
        lines = output.splitlines()
        for line in lines:
            if line.startswith("@F 0 "):
                return int(line.split()[2])
        return 0

    def parse_for_total_time(self, output):
        lines = output.splitlines()
        for line in lines:
            if line.startswith("@F 0 "):
                return float(line.split()[4])
        return 0

    def playerMaintenanceEvent(self):
        """Consumes mpg123 output while playing"""
        curr_pos = 0
        curr_time = 0.0
        while self.playing:
            with self.readWriteLock:
                output = self.player.read_very_eager()
            if not output:  # song must have stopped playing
                with self.songInfoLock:
                    self.playing = False
                    print "player thinks song is done; no output..."
                    self.location = ''
                break;
            lines = output.splitlines()
            for line in lines:
                tokens = line.split()
                if len(tokens) > 4 and tokens[0] == "@F":
                    curr_pos = int(tokens[1])
                    curr_time = float(tokens[3])
                    with self.songInfoLock:
                        self.curr_pos = curr_pos
                        self.curr_time = curr_time
            time.sleep(1)

