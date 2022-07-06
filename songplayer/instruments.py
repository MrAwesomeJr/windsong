from random import choice

class Keyboard:
    def __init__(self):
        self.notes = {("C",2): "z",
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

    def note_playable(self, pitch, force_octave=False, **kwargs):
        if pitch in self.notes:
            return True
        elif force_octave:
            if pitch[0] in map(lambda x: x[0], self.notes.keys()):
                return True
        return False

    def note_to_key(self, pitch, force_octave=False, **kwargs):
        if pitch in self.notes:
            return self.notes[pitch]
        elif force_octave:
            if pitch[1] < 2:
                return self.notes[(pitch[0],2)]
            elif pitch[1] > 4:
                return self.notes[(pitch[0],4)]

    def key_to_note(self, keyboard_note):
        for key, value in self.notes:
            if value == keyboard_note:
                return value
        return False


class Drum:
    def __init__(self):
        self.constant_notes = {"E": "A",  # (left ka)
                               "F": "L",  # (right ka)
                               "G": "S",  # (left don)
                               "A": "K"}  # (right don)

    def _random_notes(self, note):
        if note == "C":
            return choice(["A", "L"])
        elif note == "D":
            return choice(["S", "K"])
        return ""

    def note_playable(self, note, **kwargs):
        if note.pitch in self.constant_notes or note in ("C","D"):
            return True
        return False

    def note_to_key(self, note, **kwargs):
        ret = self._random_notes(note[0])
        if ret != "":
            return ret
        else:
            return self.constant_notes[note[0]]

    def key_to_note(self, drum_note):
        for key, value in self.constant_notes:
            if value == drum_note:
                return value
        return False