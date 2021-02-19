from subprocess import run
from os import chdir,kill
from getpass import getuser
import psutil

chdir("main")
run(["start","copypasta.exe"],shell=True)


import win32gui
def get_window_titles():
    ret = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            txt = win32gui.GetWindowText(hwnd)
            if txt:
                ret.append((hwnd,txt))

    win32gui.EnumWindows(winEnumHandler, None)
    return ret

#check if a window have the name copypasta, if not, close the program
while True:
    all_titles = get_window_titles()
    window_starts = lambda title: [(hwnd,full_title) for (hwnd,full_title) in all_titles if full_title.startswith(title)]
    all_matching_windows = window_starts('CopyPasta')
    if len(all_matching_windows) < 1:
        run(["taskkill","copypasta.exe"])