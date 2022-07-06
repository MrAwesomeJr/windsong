import keyboard


class KeyPress:
    def __init__(self):
        pass

    def press(self, key):
        keyboard.press_and_release(key)


class Simulator:
    def __init__(self):
        pass

    def press(self, key):
        print(key)