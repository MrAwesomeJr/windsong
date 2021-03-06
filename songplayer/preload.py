# a script to "preload" the library to prevent delay when playing an actual song.
from songplayer.song import Song
from songplayer.player import Player

def preload():
    c = Song(bpm=150)
    c.add_note(1, ("C", 2))

    player = Player()

    player.play(c, countdown=0)