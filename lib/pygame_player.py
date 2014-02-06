import time
import pygame

class PygamePlayer:
    def __init__(self):
        print "boojplayer init!"
        pygame.mixer.init()
        self.volume = pygame.mixer.music.get_volume()
        self.playing = False

    def set_location(self, location):
        #print "setting location to %s" % location
        mylocation = location
        try:
            mylocation.decode('utf-8')
        except UnicodeDecodeError:
            print "encoding utf8.."
            mylocation = location[0].encode('utf8')
        pygame.mixer.music.load(mylocation)
        # volume is reset when new music is loaded
        pygame.mixer.music.set_volume(self.volume)

    def query_position(self):
        return pygame.mixer.music.get_pos()

    def seek(self, duration):
        pygame.mixer.music.set_pos(duration)

    def pause(self):
        pygame.mixer.music.pause()
        self.playing = False

    def unpause(self):
        pygame.mixer.music.unpause()
        self.playing = True 

    def play(self):
        print("player playin' g!")
        pygame.mixer.music.play()
        self.playing = True

    def stop(self):
        print("stopped player")
        pygame.mixer.music.stop()
        self.playing = False

    def is_playing(self):
        return self.playing

    def get_volume(self):
        return pygame.mixer.music.get_volume()

    def set_volume(self, vol):
        self.volume = vol
        pygame.mixer.music.set_volume(self.volume)

