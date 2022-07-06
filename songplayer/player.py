import time
from songplayer import instruments, outputs

default_countdown = 5


class StaticTimer:
    def __init__(self):
        pass

    def wait(self, start_time, note_index, song, debug):
        note = song.data[note_index]
        time_elapsed = time.perf_counter() - start_time
        beat_time = note.beat / (song.bpm / 60)

        if beat_time <= time_elapsed:
            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))

        else:
            time_until_beat = beat_time - time_elapsed
            while time_until_beat > 0:
                time_elapsed = time.perf_counter() - start_time
                time_until_beat = beat_time - time_elapsed

            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))


class RelativeTimer:
    def __init__(self):
        pass

    def wait(self, start_time, note_index, song, debug):
        note = song.data[note_index]
        previous_beat_time = 0
        if note_index > 0:
            previous_beat_time = song.data[note_index - 1].beat / (song.bpm / 60)

        time_elapsed = time.perf_counter() - start_time
        beat_time = time_elapsed + (note.beat / (song.bpm / 60)) - previous_beat_time

        if beat_time <= time_elapsed:
            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))

        else:
            time_until_beat = beat_time - time_elapsed
            time.sleep(time_until_beat)
            time_elapsed = time.perf_counter() - start_time

            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))


class Player:
    def __init__(self, instrument=instruments.Keyboard(), player=StaticTimer(), output=outputs.KeyPress()):
        self.instrument = instrument
        self.player = player
        self.output = output

    def play(self, song, countdown: int = default_countdown, end_playback_beat=None, loops=1, debug=False, **kwargs):
        song = song.sorted_song()
        while loops != 0:
            if countdown > 0:
                time.sleep(countdown)
            start_time = time.perf_counter()

            for index, note in enumerate(song.data):
                if end_playback_beat != None and note.beat >= end_playback_beat:
                    break

                if self.instrument.note_playable(note.pitch, **kwargs):
                    self.player.wait(start_time, index, song, debug)
                    self.output.press(self.instrument.note_to_key(note.pitch, **kwargs))
                elif debug:
                    print(str(note) + " Note Unplayable")

            loops -= 1