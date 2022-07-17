import time
from songplayer import timer
from songplayer import instruments, output
import logging


class Player:
    def __init__(self, instrument=instruments.Keyboard(), timer=timer.StaticTimer(), output=output.KeyPress()):
        self.instrument = instrument
        self.timer = timer
        self.output = output
        self.logger = logging.getLogger("player")

    def play(self, song, countdown=5, start_playback_beat=0, end_playback_beat=None, loops=1, **kwargs):
        song = song.sorted_song()

        while loops != 0:
            if countdown > 0:
                time.sleep(countdown)
            self.timer.start()

            self.logger.info(f"Song start time: {self.timer.start_time}")

            for index, note in enumerate(song.data):
                if end_playback_beat is not None and note.beat >= end_playback_beat:
                    break
                elif note.beat < start_playback_beat:
                    self.logger.debug(f"{note} Note Skipped")
                    continue

                if self.instrument.note_playable(note.pitch, **kwargs):
                    self.timer.wait(index, song)
                    self.output.press(self.instrument.note_to_key(note.pitch, **kwargs))
                else:
                    self.logger.debug(f"{note} Note Unplayable")

            self.timer.end()
            loops -= 1