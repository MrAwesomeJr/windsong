import time
import ntplib
import socket


class BaseTimer:
    def __init__(self):
        self.start_time = 0

    def start(self):
        self.start_time = time.perf_counter()


class StaticTimer(BaseTimer):
    def wait(self, note_index, song, debug):
        note = song.data[note_index]
        time_elapsed = time.perf_counter() - self.start_time
        beat_time = note.beat / (song.bpm / 60)

        if beat_time <= time_elapsed:
            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))

        else:
            time_until_beat = beat_time - time_elapsed
            while time_until_beat > 0:
                time_elapsed = time.perf_counter() - self.start_time
                time_until_beat = beat_time - time_elapsed

            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))


class RelativeTimer(BaseTimer):
    def wait(self, note_index, song, debug):
        note = song.data[note_index]
        previous_beat_time = 0
        if note_index > 0:
            previous_beat_time = song.data[note_index - 1].beat / (song.bpm / 60)

        time_elapsed = time.perf_counter() - self.start_time
        beat_time = time_elapsed + (note.beat / (song.bpm / 60)) - previous_beat_time

        if beat_time <= time_elapsed:
            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))

        else:
            time_until_beat = beat_time - time_elapsed
            time.sleep(time_until_beat)
            time_elapsed = time.perf_counter() - self.start_time

            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))


class NetTimer_OnInit:
    def __init__(self, addr):
        self.start_time = 0
        self.desync = 0
        self.get_server_desync(addr)
        self.addr = addr

    def get_server_desync(self, addr):
        c = ntplib.NTPClient()
        if addr is None:
            response = c.request(self.addr[0])
        else:
            response = c.request(addr[0])
        self.desync = response.offset

    def start(self):
        s = socket.socket()
        s.connect(self.addr)
        self.start_time = float(s.recv(1024).decode())
        s.shutdown(socket.SHUT_RDWR)
        s.close()

    def wait(self, note_index, song, debug):
        note = song.data[note_index]
        time_elapsed = time.time() - self.start_time
        beat_time = note.beat / (song.bpm / 60)

        if beat_time <= time_elapsed:
            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))

        else:
            time_until_beat = beat_time - time_elapsed
            while time_until_beat > 0:
                time_elapsed = time.time() - self.start_time
                time_until_beat = beat_time - time_elapsed

            if debug:
                print(note, "dt:" + str(time_elapsed - beat_time))

class NetTimer():
    def wait(self):
        pass