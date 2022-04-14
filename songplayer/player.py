import time
import keyboard


class TimedPlayer:
    def __init__(self, song):
        self.song = song

    def play_lyre(self, countdown: int = 5, debug=False):
        lyre_notes = {("C",2): "z",
                      ("D",2): "x",
                      ("E",2): "c",
                      ("F",2): "v",
                      ("G",2): "b",
                      ("A",2): "n",
                      ("B",2): "m",
                      ("C",3): "a",
                      ("D",3): "s",
                      ("E",3): "d",
                      ("F",3): "f",
                      ("G",3): "g",
                      ("A",3): "h",
                      ("B",3): "j",
                      ("C",4): "q",
                      ("D",4): "w",
                      ("E",4): "e",
                      ("F",4): "r",
                      ("G",4): "t",
                      ("A",4): "y",
                      ("B",4): "u"}
        self.song = self.song.sorted_song()
        time.sleep(countdown)
        start_time = time.perf_counter()
        time_elapsed = 0
        previous_time = time_elapsed
        for note in self.song.data:
            if note.pitch in lyre_notes:
                beat_time = note.beat / (self.song.bpm / 60)
                time_elapsed = time.perf_counter() - start_time
                if beat_time <= time_elapsed:
                    previous_time = time_elapsed
                    if debug:
                        print(note,"dt:"+str(time_elapsed-beat_time))
                    keyboard.press(lyre_notes[note.pitch])
                    keyboard.release(lyre_notes[note.pitch])

                else:
                    time_until_beat = beat_time - time_elapsed
                    while time_until_beat > 0:
                        time.sleep(time_until_beat / 2)
                        time_elapsed = time.perf_counter() - start_time
                        time_until_beat = beat_time - time_elapsed

                    if debug:
                            print(note,"dt:"+str(time_elapsed-beat_time))
                    keyboard.press_and_release(lyre_notes[note.pitch])
            elif debug:
                print(str(note) + " Note Unplayable")

class SmoothPlayer:
    def __init__(self, song):
        self.song = song

    def play_lyre(self, countdown: int = 5, debug=False):
        lyre_notes = {("C",2): "z",
                      ("D",2): "x",
                      ("E",2): "c",
                      ("F",2): "v",
                      ("G",2): "b",
                      ("A",2): "n",
                      ("B",2): "m",
                      ("C",3): "a",
                      ("D",3): "s",
                      ("E",3): "d",
                      ("F",3): "f",
                      ("G",3): "g",
                      ("A",3): "h",
                      ("B",3): "j",
                      ("C",4): "q",
                      ("D",4): "w",
                      ("E",4): "e",
                      ("F",4): "r",
                      ("G",4): "t",
                      ("A",4): "y",
                      ("B",4): "u"}

        keyboard = Controller()

        self.song = self.song.sorted_song()
        time.sleep(countdown)
        beat_time = 0
        for note in self.song.data:
            if note.pitch in lyre_notes:
                previous_beat_time = beat_time
                beat_time = note.beat / (self.song.bpm / 60)
                if beat_time > previous_beat_time:
                    time.sleep(beat_time - previous_beat_time)
                    if debug:
                            print(note)
                    keyboard.press(lyre_notes[note.pitch])
                    keyboard.release(lyre_notes[note.pitch])
            elif debug:
                print(str(note) + " Note Unplayable")
