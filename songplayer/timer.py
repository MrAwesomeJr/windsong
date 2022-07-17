import time
import ntplib
import socket
import threading
import queue
import subprocess
import os
from numpy import mean, std
import logging


class BaseTimer:
    def __init__(self):
        self.logger = logging.getLogger("timer")
        self.start_time = 0

    def start(self):
        self.start_time = time.perf_counter()

    def end(self):
        pass


class StaticTimer(BaseTimer):
    def wait(self, note_index, song):
        note = song.data[note_index]
        time_elapsed = time.perf_counter() - self.start_time
        beat_time = note.beat / (song.bpm / 60)

        if beat_time <= time_elapsed:
            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")

        else:
            time_until_beat = beat_time - time_elapsed
            while time_until_beat > 0:
                time_elapsed = time.perf_counter() - self.start_time
                time_until_beat = beat_time - time_elapsed

            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")


class RelativeTimer(BaseTimer):
    def wait(self, note_index, song):
        note = song.data[note_index]
        previous_beat_time = 0
        if note_index > 0:
            previous_beat_time = song.data[note_index - 1].beat / (song.bpm / 60)

        time_elapsed = time.perf_counter() - self.start_time
        beat_time = time_elapsed + (note.beat / (song.bpm / 60)) - previous_beat_time

        if beat_time <= time_elapsed:
            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")

        else:
            time_until_beat = beat_time - time_elapsed
            time.sleep(time_until_beat)
            time_elapsed = time.perf_counter() - self.start_time

            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")


class NetTimerOnInit(BaseTimer):
    def __init__(self, addr):
        super().__init__()
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
        self.start_time = ""
        while self.start_time == "":
            self.start_time = s.recv(1024).decode()
        self.start_time = float(self.start_time)
        self.logger.info(f"Start time received of {self.start_time}")
        s.shutdown(socket.SHUT_RDWR)
        s.close()

    def wait(self, note_index, song):
        note = song.data[note_index]
        time_elapsed = time.time() - (self.start_time - self.desync)
        beat_time = note.beat / (song.bpm / 60)

        if beat_time <= time_elapsed:
            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")

        else:
            time_until_beat = beat_time - time_elapsed
            while time_until_beat > 0:
                time_elapsed = time.time() - (self.start_time - self.desync)
                time_until_beat = beat_time - time_elapsed

            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")


class NetTimer(BaseTimer):
    class Ping:
        def __init__(self, server_addr, game_addr):
            self.logger = logging.getLogger("timer")
            self.desync = 0
            self.is_continue = threading.Event()
            self.is_continue.set()
            self.received_start = threading.Event()
            self.desync_queue = queue.Queue(maxsize=1)

            self.server_addr = server_addr
            self.game_addr = game_addr

            # ping_list is used by ping_loop and ping_server in the thread.
            self.ping_list = []

            self.socket = socket.socket()
            self.socket.connect(self.server_addr)

            self.thread = threading.Thread(target=self.ping_loop, args=())
            self.thread.start()
            self.logger.info("Pinging thread started")

        def get_desync(self):
            if not self.desync_queue.empty():
                self.desync = float(self.desync_queue.get())
            return self.desync

        def stop_pinging(self):
            self.is_continue.clear()
            self.thread.join()
            self.socket.close()

        def ping_loop(self):
            start_time = time.perf_counter()
            self.ping_server(self.game_addr[0])
            while self.is_continue.is_set():
                # loop many times per ping (to have additional chances to end thread).
                # precision of sleep doesn't matter since total wait time is arbitrary.
                if (time.perf_counter() - start_time) >= 5:
                    self.ping_server(self.game_addr[0])
                else:
                    # give time for other threads to run
                    time.sleep(0.1)
            self.logger.info(f"Pinging thread ended")

        def get_ntp_desync(self):
            c = ntplib.NTPClient()
            response = c.request(self.server_addr[0])
            return response.offset

        def ping_server(self, ip):
            # at the moment songplayer is only used with windows
            # but if i / mihoyo ever decide to update then this is good futureproofing.
            if os.name == "nt":
                result = subprocess.run("ping -n 1 "+ip, capture_output=True, text=True)
                if result.returncode == 0:
                    ping = result.stdout.split("Average = ")
                    ping = ping[-1]
                    # output should be of format "123ms\n"
                    ping = float(ping.split("ms\n")[0])

            elif os.name == "posix":
                result = subprocess.run("ping -c 1 "+ip, capture_output=True, text=True)
                if result.returncode == 0:
                    ping = result.stdout.split("min/avg/max/stddev = ")
                    ping = ping[-1]
                    # output should be of format "123/123/123/0.000 ms\n"
                    ping = float(ping.split("/")[1])
            else:
                raise OSError("Operating System not supported.")

            ping = ping / 1000.0
            self.logger.debug(f"Ping received of {ping}")

            if result.returncode == 0:
                self.ping_list.append(ping)
                current_ping = self.ping_list[-1]
                if len(self.ping_list) > 10:
                    self.ping_list.pop(0)

                dev_margin = 1.5
                # ignore pings that are outside of dev_margin standard deviations to remove spikes.
                for ping in reversed(self.ping_list):
                    if ping > (mean(self.ping_list) + std(self.ping_list) * dev_margin) or ping < (mean(self.ping_list) - std(self.ping_list) * dev_margin):
                        continue
                    else:
                        current_ping = ping
                        break
            else:
                self.logger.warning(f"Ping command failed")

            if self.received_start.is_set():
                # blocking request from server
                self.socket.send(str(current_ping).encode())
                self.logger.debug(f"Ping sent of {current_ping}")
                desync = ""
                while desync == "":
                    desync = self.socket.recv(1024).decode()

                if desync == "NTP":
                    desync = self.get_ntp_desync()
                else:
                    desync = float(desync)
                    
                self.logger.debug(f"Desync received of {desync}")

                if self.desync_queue.full():
                    self.desync_queue.get()
                self.desync_queue.put(desync)

    def __init__(self, server_addr, game_addr):
        super().__init__()
        self.server_addr = server_addr
        self.game_addr = game_addr
        self.ping = None

    def start(self):
        self.ping = self.Ping(self.server_addr, self.game_addr)
        self.start_time = ""
        while self.start_time == "":
            self.start_time = self.ping.socket.recv(1024).decode()
        self.start_time = float(self.start_time)
        self.logger.info(f"Start time received of {self.start_time}")
        self.ping.received_start.set()

    def end(self):
        self.ping.stop_pinging()

    def wait(self, note_index, song):
        note = song.data[note_index]
        time_elapsed = time.time() - (self.start_time - self.ping.get_desync())
        beat_time = note.beat / (song.bpm / 60)

        if beat_time <= time_elapsed:
            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")

        else:
            time_until_beat = beat_time - time_elapsed
            while time_until_beat > 0:
                time_elapsed = time.time() - (self.start_time - self.ping.get_desync())
                time_until_beat = beat_time - time_elapsed

            self.logger.info(f"{note} dt:{time_elapsed - beat_time}")
