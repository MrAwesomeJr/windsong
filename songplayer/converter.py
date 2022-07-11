from songplayer.song import Song
import mido


def text_to_data(text):
    info, notes = text.split("\n\n")
    info = info.split("\n")
    notes = notes.split("\n")
    bpm = 0
    time_signature = [0,0]
    for line in info:
        if line[:3] == "bpm":
            bpm = float(line[4:])
        elif line[:14] == "time_signature":
            time_signature = list(map(int, line[15:].split("/")))

    song = Song(bpm, time_signature)

    for line in notes:
        # commenting
        if line[:2] == "//":
            continue
        elif line == "":
            continue
        else:
            beat, key, octave = line.split(" ")
            song.add_note(float(beat), (key,int(octave)))

    return song


def data_to_text(song):
    text = "bpm " + str(song.bpm)
    text += "\n" + "time_signature " + str(song.time_signature[0]) + "/" + str(song.time_signature[1]) +"\n"
    for note in song.data:
        if int(note.beat) == note.beat:
            beat = int(note.beat)
        else:
            beat = note.beat
        text += "\n" + str(beat) + " " + note.pitch[0] + " " + str(note.pitch[1])
    return text


def midi_to_data(filename, track=0, tracks=[], truncate_silence=False, transpose_semitones=0, round_beats=False, rounding_precision = 1/16):
    # round_beats rounds to the nearest given fraction of a beat when converting from ms into beats
    mid = mido.MidiFile(filename)
    bpm = 0
    time_signature = [0,0]
    track_indexes = []
    keys = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    for index, msg in enumerate(mid):
        if msg.is_meta:
            if msg.type == "time_signature":
                time_signature = [msg.numerator, msg.denominator]
            elif msg.type == "set_tempo":
                bpm = mido.tempo2bpm(msg.tempo)
            elif msg.type == "track_name":
                track_indexes.append(index)

    song = Song(bpm, time_signature)

    if len(tracks) == 0:
        midi_track = mid.tracks[track]
        track_time_elapsed = 0
        key = "C"
        octave = 0
        for msg in midi_track:
            if truncate_silence and len(song.data) == 0:
                pass
            else:
                track_time_elapsed += msg.time

            # msg.note is the scale where 0 is C-2 and 72 is C4
            # msg.time is the time difference since the last msg or the start in arbitrary "ticks"
            # see https://mido.readthedocs.io/en/latest/midi_files.html#tempo-and-beat-resolution
            if msg.type == "note_on" and msg.velocity != 0:
                key = keys[(msg.note + transpose_semitones) % 12]
                octave = (msg.note + transpose_semitones) // 12 - 2
                beat = track_time_elapsed / mid.ticks_per_beat
                if round_beats:
                    beat = round(beat / rounding_precision) * rounding_precision

                song.add_note(beat, (key, octave))

    else:
        for track_index in tracks:
            midi_track = mid.tracks[track_index]
            track_time_elapsed = 0
            key = "C"
            octave = 0
            for msg in midi_track:
                if truncate_silence and len(song.data) == 0:
                    pass
                else:
                    track_time_elapsed += msg.time

                # msg.note is the scale where 0 is C-2 and 72 is C4
                # msg.time is the time difference since the last msg or the start in arbitrary "ticks"
                # see https://mido.readthedocs.io/en/latest/midi_files.html#tempo-and-beat-resolution
                if msg.type == "note_on" and msg.velocity != 0:
                    key = keys[(msg.note + transpose_semitones) % 12]
                    octave = (msg.note + transpose_semitones) // 12 - 2
                    beat = track_time_elapsed / mid.ticks_per_beat
                    if round_beats:
                        beat = round(beat / rounding_precision) * rounding_precision

                    song.add_note(beat, (key, octave))

            song.sort()


    return song