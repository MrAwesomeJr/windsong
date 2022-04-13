# from pynput.keyboard import Controller
# from time import sleep
# keyboard = Controller()
#
# for i in range(100):
#     sleep(0.2)
#     keyboard.press("a")
#     keyboard.release("a")

import keyboard
from time import sleep
for i in range(100):
    sleep(0.2)
    keyboard.press_and_release("q")
    keyboard.press_and_release("a")
    keyboard.press_and_release("f")