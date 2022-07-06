import time


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


class NetTimer:
    def __init__(self):
        pass

    def wait(self, start_time, note_index, song, debug):
        note = song.data[note_index]
        time_elapsed = time.time() - start_time
        beat_time = note.beat / (song.bpm / 60)

        if beat_time <= time_elapsed:
            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))

        else:
            time_until_beat = beat_time - time_elapsed
            while time_until_beat > 0:
                time_elapsed = time.time() - start_time
                time_until_beat = beat_time - time_elapsed

            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))
