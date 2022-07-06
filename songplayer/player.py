import time
from songplayer import timer
from songplayer import instruments, outputs
import ntplib
import socket


class Player:
    def __init__(self, instrument=instruments.Keyboard(), timer=timer.StaticTimer(), output=outputs.KeyPress()):
        self.instrument = instrument
        self.timer = timer
        self.output = output

    def play(self, song, countdown=5, end_playback_beat=None, loops=1, debug=False, **kwargs):
        song = song.sorted_song()
        while loops != 0:
            if countdown > 0:
                time.sleep(countdown)
            start_time = time.perf_counter()

            for index, note in enumerate(song.data):
                if end_playback_beat is not None and note.beat >= end_playback_beat:
                    break

                if self.instrument.note_playable(note.pitch, **kwargs):
                    self.timer.wait(start_time, index, song, debug)
                    self.output.press(self.instrument.note_to_key(note.pitch, **kwargs))
                elif debug:
                    print(str(note) + " Note Unplayable")

            loops -= 1


class NetPlayerStart:
    def __init__(self, addr, instrument=instruments.Keyboard(), output=outputs.KeyPress()):
        self.addr = addr
        self.instrument = instrument
        self.timer = timer.NetTimer()
        self.output = output
        self.desync = 0

    def get_server_desync(self, addr=None):
        c = ntplib.NTPClient()
        if addr is None:
            response = c.request(self.addr[0])
        else:
            response = c.request(addr[0])
        self.desync = response.offset

    def play(self, song, countdown=5, end_playback_beat=None, loops=1, debug=False, **kwargs):

        while loops != 0:
            if countdown > 0:
                time.sleep(countdown)

            song = song.sorted_song()

            s = socket.socket()
            s.connect(self.addr)
            start_time = float(s.recv(1024).decode())
            s.shutdown(socket.SHUT_RDWR)
            s.close()

            for index, note in enumerate(song.data):
                if end_playback_beat is not None and note.beat >= end_playback_beat:
                    break

                if self.instrument.note_playable(note.pitch, **kwargs):
                    self.timer.wait(start_time, index, song, debug)
                    self.output.press(self.instrument.note_to_key(note.pitch, **kwargs))
                elif debug:
                    print(str(note) + " Note Unplayable")

            loops -= 1
