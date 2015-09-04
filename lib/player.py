from booj.models import model

class BoojPlayer:
    def __init__(self):
        pass

    def set_location(self, location):
        """
        Queue up a song to play next.  This takes a string
        of the absolute path to the resource.

        Be careful! If your let your song run to completion
        you will no longer have a location set.  The files
        you load are "clear on complete"

        Returns the length of the song in seconds as a float.

        """
        return 0.0

    def query_position(self):
        """Returns a Position object with the following members:
            * the current position as a float that is
              the percentage of the way through the song.
            * the current time in seconds
            * the song length in seconds
        """
        return Position()

    def seek(self, position):
        """Jump to the specified position.
        Position is specified by a percentage (float) value.
        """
        pass

    def pause(self):
        """Pauses current song in progress.  Does nothing if
        no song is playing.
        """
        pass

    def unpause(self):
        """Unpauses current song in progress.  Does nothing if
        no song is loaded.
        """
        pass

    def play(self):
        """Play your song.
        A file location must have been specified first.
        But note that you must also call play; songs do 
        not automagically start playing on load.

        """
        pass

    def stop(self):
        """Pauses current song in progress.  Same as pause.
        """
        pass

    def is_playing(self):
        """Returns True if a song is currently playing,
        false otherwise.
        """
        return False

    def get_volume(self):
        """Returns analog volume as an integer percentage, 0-100.
        """
        return 0

    def set_volume(self, vol):
        """This function sets the analog volume using
        the ALSA soundcard driver. Vol is an integer
        percentage, 0-100.

        """
        pass

