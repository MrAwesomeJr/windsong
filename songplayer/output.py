import keyboard
import os
from songplayer.focus_genshin import focus_genshin
import logging


class KeyPress:
    def __init__(self):
        pass

    def press(self, key):
        keyboard.press_and_release(key)


class AutoSwitchKeyPress:
    def __init__(self):
        focus_genshin()

    def press(self, key):
        keyboard.press_and_release(key)


class Simulator:
    def __init__(self):
        self.logger = logging.getLogger("output")

    def press(self, key):
        self.logger.info(f"Key Simulated {key}")