import os

if os.name == "nt":
    import win32gui
    import win32con
    import win32api


def focus_genshin():
    if os.name != "nt":
        raise ImportError("AutoSwitchKeyPress relies on win32.")

    target_window = win32gui.FindWindow("UnityWndClass", None)
    win32gui.SetForegroundWindow(target_window)
