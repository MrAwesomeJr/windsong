import keyboard
import os

if os.name == "nt":
    import win32gui
    import win32con
    import win32api


class KeyPress:
    def __init__(self):
        pass

    def press(self, key):
        keyboard.press_and_release(key)

class AutoSwitchKeyPress:
    def __init__(self):
        if os.name != "nt":
            raise ImportError("AutoSwitchKeyPress relies on win32.")

        self.target_window = win32gui.FindWindow("UnityWndClass", None)
        win32gui.SetForegroundWindow(self.target_window)


    def press(self, key):
        keyboard.press_and_release(key)

class Simulator:
    def __init__(self):
        pass

    def press(self, key):
        print(key)