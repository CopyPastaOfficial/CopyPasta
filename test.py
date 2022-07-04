# keep main window hidden
from tkinter import Tk
from tkinter.filedialog import askopenfile


Tk().withdraw()
# open file dialog
file_path = askopenfile(mode = "r")