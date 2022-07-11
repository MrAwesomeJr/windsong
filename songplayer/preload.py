# a script to "preload" the library to prevent delay when playing an actual song.
from songplayer.song import Song
from songplayer.player import Player


def preload(note=("C", 2), player=Player()):
    song = Song(bpm=150)
    song.add_note(1, note)

    player.play(song, countdown=0)