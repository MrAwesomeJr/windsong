# a script to "preload" the library to prevent delay when playing an actual song.
from songplayer.song import Song
from songplayer.player import Player
import logging

preload_logger = logging.getLogger("preload")


def preload(note=("C", 2), player=Player()):
    song = Song(bpm=150)
    song.add_note(1, note)

    player.play(song, countdown=0)

    preload_logger.info("Library preloaded")
