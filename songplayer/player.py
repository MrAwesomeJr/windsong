import time
import keyboard
from songplayer.noteconverter import NoteConverter

default_countdown = 5


class TimedPlayer:
    def __init__(self):
        self.noteconverter = NoteConverter()

    def play_keyboard(self, song, countdown: int = default_countdown, end_playback_beat=None, loops=1, debug=False):
        song = song.sorted_song()
        while loops != 0:
            time.sleep(countdown)
            start_time = time.perf_counter()
            time_elapsed = 0
            previous_time = time_elapsed
            for note in song.data:
                if end_playback_beat != None and note.beat >= end_playback_beat:
                    break
                if note.pitch in self.noteconverter.keyboard.notes:
                    beat_time = note.beat / (song.bpm / 60)
                    time_elapsed = time.perf_counter() - start_time
                    if beat_time <= time_elapsed:
                        previous_time = time_elapsed
                        if debug:
                            print(note,"dt:"+str(time_elapsed - beat_time))
                        keyboard.press_and_release(self.noteconverter.keyboard.note_to_key(note.pitch))

                    else:
                        time_until_beat = beat_time - time_elapsed
                        while time_until_beat > 0:
                            time.sleep(time_until_beat / 2)
                            time_elapsed = time.perf_counter() - start_time
                            time_until_beat = beat_time - time_elapsed

                        if debug:
                            print(note,"dt:"+str(time_elapsed - beat_time))
                        keyboard.press_and_release(self.noteconverter.keyboard.note_to_key(note.pitch))
                elif debug:
                    print(str(note) + " Note Unplayable")

            loops -= 1

    def play_drum(self, song, countdown: int = default_countdown, end_playback_beat=None, loops=1, debug=False):
        song = song.sorted_song()
        while loops != 0:
            time.sleep(countdown)
            start_time = time.perf_counter()
            time_elapsed = 0
            previous_time = time_elapsed
            for note in song.data:
                if end_playback_beat != None and note.beat >= end_playback_beat:
                    break
                if note.pitch in self.noteconverter.keyboard.notes:
                    beat_time = note.beat / (song.bpm / 60)
                    time_elapsed = time.perf_counter() - start_time
                    if beat_time <= time_elapsed:
                        previous_time = time_elapsed
                        if debug:
                            print(note,"dt:"+str(time_elapsed - beat_time))
                        keyboard.press_and_release(self.noteconverter.drum.note_to_key(note.pitch))

                    else:
                        time_until_beat = beat_time - time_elapsed
                        while time_until_beat > 0:
                            time.sleep(time_until_beat / 2)
                            time_elapsed = time.perf_counter() - start_time
                            time_until_beat = beat_time - time_elapsed

                        if debug:
                            print(note,"dt:"+str(time_elapsed - beat_time))
                        keyboard.press_and_release(self.noteconverter.drum.note_to_key(note.pitch))
                elif debug:
                    print(str(note) + " Note Unplayable")

            loops -= 1


class SmoothPlayer:
    def __init__(self):
        self.noteconverter = NoteConverter()

    def play_keyboard(self, song, countdown: int = default_countdown, end_playback_beat=None, loops=1, debug=False):
        song = song.sorted_song()
        while loops != 0:
            time.sleep(countdown)
            beat_time = 0
            for note in song.data:
                if end_playback_beat != None and note.beat >= end_playback_beat:
                    break
                if note.pitch in self.noteconverter.keyboard.notes:
                    time_since_last_beat = time.perf_counter()
                    #init timer (actualized after sleep function)
                    previous_beat_time = beat_time
                    beat_time = note.beat / (song.bpm / 60)
                    if beat_time > previous_beat_time:
                        time.sleep(beat_time - previous_beat_time)
                        time_since_last_beat -= time.perf_counter()
                        if debug:
                            print(note,"dt:"+str(beat_time - time_since_last_beat))
                        keyboard.press_and_release(self.noteconverter.keyboard.note_to_key(note.pitch))
                    else:
                        keyboard.press_and_release(self.noteconverter.keyboard.note_to_key(note.pitch))
                elif debug:
                    print(str(note) + " Note Unplayable")

            loops -= 1

    def play_drum(self, song, countdown: int = default_countdown, end_playback_beat=None, loops=1, debug=False):
        song = song.sorted_song()
        while loops != 0:
            time.sleep(countdown)
            beat_time = 0
            for note in song.data:
                if end_playback_beat != None and note.beat >= end_playback_beat:
                    break
                if note.pitch in self.noteconverter.keyboard.notes:
                    time_since_last_beat = time.perf_counter()
                    #init timer (actualized after sleep function)
                    previous_beat_time = beat_time
                    beat_time = note.beat / (song.bpm / 60)
                    if beat_time > previous_beat_time:
                        time.sleep(beat_time - previous_beat_time)
                        time_since_last_beat -= time.perf_counter()
                        if debug:
                            print(note,"dt:"+str(beat_time - time_since_last_beat))
                        keyboard.press_and_release(self.noteconverter.drum.note_to_key(note.pitch))
                    else:
                        keyboard.press_and_release(self.noteconverter.drum.note_to_key(note.pitch))
                elif debug:
                    print(str(note) + " Note Unplayable")

            loops -= 1
