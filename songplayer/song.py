class Song:
    class Note:
        def __init__(self, beat: float, pitch):
            #pitch is composed of tuple (<key>,<octave>)
            self.beat = beat
            self.pitch = pitch

        def __str__(self):
            if int(self.beat) == self.beat:
                return_string = str(int(self.beat)).ljust(20) + str(self.pitch[0]).ljust(3) + str(self.pitch[1])
            else:
                return_string = str(self.beat).ljust(20) + str(self.pitch[0]).ljust(3) + str(self.pitch[1])
            return return_string

    def __init__(self, bpm: float = 60, time_signature=[4, 4], data=None):
        self.bpm = bpm
        self.time_signature = time_signature
        if data == None:
            # apparently you can't initialize empty lists as function default arguments
            self.data = []
        else:
            self.data = data

    def __str__(self):
        return_string = str(self.bpm)
        for note in self.data:
            return_string += str(note) + "\n"
        return return_string

    def add_note(self, beat: float, pitch, bar=1):
        self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), pitch))

    def add_drum_note(self, beat: float, note, hand="random", bar=1):
        # note accepts "don" and "ka"
        # hand accepts "random", "left" and "right"

        if note == "don":
            if hand == "random":
                self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), ("D", 3)))
            elif hand == "left":
                self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), ("G", 3)))
            elif hand == "right":
                self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), ("A", 3)))
        elif note == "ka":
            if hand == "random":
                self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), ("C", 3)))
            elif hand == "left":
                self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), ("E", 3)))
            elif hand == "right":
                self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), ("F", 3)))


    def add_keyboard_note(self, beat, key, bar=0):
        keyboard_notes = {"z": ("C",2),
                      "x": ("D",2),
                      "c": ("E",2),
                      "v": ("F",2),
                      "b": ("G",2),
                      "n": ("A",2),
                      "m": ("B",2),
                      "a": ("C",3),
                      "s": ("D",3),
                      "d": ("E",3),
                      "f": ("F",3),
                      "g": ("G",3),
                      "h": ("A",3),
                      "j": ("B",3),
                      "q": ("C",4),
                      "w": ("D",4),
                      "e": ("E",4),
                      "r": ("F",4),
                      "t": ("G",4),
                      "y": ("A",4),
                      "u": ("B",4)}

        self.data.append(self.Note(beat + ((bar - 1) * self.time_signature[0]), keyboard_notes[key]))

    def append_song(self, song, beat_offset=None, beat_offset_relative=0, inherit_bpm=False, inherit_time_signature=False, sort=True):
        if beat_offset == None:
            #set beat offset to the start of the next bar
            if len(self.data) > 0:
                beat_offset = self.time_signature[0] * (self.data[-1].beat // self.time_signature[0])
            else:
                beat_offset = 0
        if inherit_bpm:
            self.bpm = song.bpm
        if inherit_time_signature:
            self.time_signature = song.time_signature

        beat_offset += beat_offset_relative
        for i, note in enumerate(song.data):
            new_song_note = note
            new_song_note.beat += beat_offset
            self.data.append(new_song_note)

        if sort:
            self.sort()

    def sort(self):
        self.data = sorted(self.data, key=lambda note: note.beat)

    def sorted_song(self):
        return Song(self.bpm, self.time_signature, sorted(self.data, key=lambda note: note.beat))