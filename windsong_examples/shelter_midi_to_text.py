import songplayer
import os

try:
    os.remove("resources/shelter")
except FileNotFoundError:
    pass

shelter = songplayer.converter.midi_to_data("resources/LyricWulf - Shelter.mid.mid",
                                            track=2,
                                            truncate_silence=True,
                                            transpose_semitones=0)

text = songplayer.converter.data_to_text(shelter)

file = open("resources/shelter", "w+")
file.write(text)
file.close()
