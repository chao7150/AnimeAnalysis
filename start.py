import tkinter as tk
from tkinter import filedialog

def start():
    filename = filedialog.askopenfilename()
    startframe = int(input("START FRAME? :"))
    endframe = int(input("END FRAME? :"))

    return (filename, startframe, endframe)    
