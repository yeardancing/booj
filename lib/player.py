import os, time 
import telnetlib

class BoojPlayer:
    def __init__(self):
        self.player = telnetlib.Telnet("localhost", "mpg123", 60)
        self.player.read_until("\n")
        self.set_volume(100)
        self.curr_pos = 0
        self.max_pos = 0
        self.total_time = 0
        self.playing = False

    def set_location(self, location):
        print type(location)
        try:
            mylocation = location.encode('ascii', 'ignore')
        except UnicodeDecodeError:
            mylocation = location[0].encode('utf8')
        self.player.write("L " + mylocation + "\n")
        self.player.write("P\n")
        load_output = self.player.read_until("@P 1\n")
        self.max_pos = self.parse_for_last_frame(load_output)
        self.total_time = self.parse_for_total_time(load_output)
        self.player.write("J 0\n")
        self.player.read_until("@J 0\n")
        self.curr_pos = 0

    def query_position(self):
        return self.curr_pos

    def seek(self, duration):
        framejump = (self._max_pos / self.total_time) * duration
        self.player.write("J framejump\n")
        self.player.read_until("@J 0\n")

    def pause(self):
        self.player.write("P\n")
        self.player.read_until("@P 1\n")
        self.playing = False

    def unpause(self):
        self.player.write("P\n")
        self.player.read_until("@P 2\n")
        self.playing = True 

    def play(self):
        self.unpause()
        self.playing = True

    def stop(self):
        self.pause()
        self.playing = False

    def is_playing(self):
        return self.playing

    def get_volume(self):
        return self.volume

    def set_volume(self, vol):
        self.volume = vol
        volume_cmd = "amixer sset PCM,0 %d%%" % (self.volume)
        os.system(volume_cmd)

    def parse_for_last_frame(self, output):
        lines = output.splitlines()
        for line in lines:
            if line.startswith("@F 0 "):
                return line.split()[2]
        return 0

    def parse_for_total_time(self, output):
        lines = output.splitlines()
        for line in lines:
            if line.startswith("@F 0 "):
                return line.split()[4]
        return 0

