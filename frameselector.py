import numpy as np
import cv2
import tkinter as tk
from tkinter import filedialog

#グローバル
SKIP_ARRAY = [-14400, -1440, -240, -24, -10, -1, 1, 10, 24, 240, 1440, 14400]
SKIP_TEXT  = ["10m", "1m", "10s", "1s", "10f", "1f", "1f", "10f", "1s", "10s", "1m", "10m"]
SIZE = (480, 270)

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        f0 = tk.Frame(self)
        self.cm_button = tk.Button(f0, text = "choose movie file", command = self.choose_movie) #Applicationが親
        self.cm_button.pack()
        f0.pack()

        f1 = tk.Frame(self)
        self.skip_buttons = [0]*12
        self.start_button = tk.Button(f1, text = u"←", command = lambda:self.skip(- self.win.getframe()))
        self.skip_buttons[0] = tk.Button(f1, text = SKIP_TEXT[0], command = lambda:self.skip(SKIP_ARRAY[0]))
        self.skip_buttons[1] = tk.Button(f1, text = SKIP_TEXT[1], command = lambda:self.skip(SKIP_ARRAY[1]))
        self.skip_buttons[2] = tk.Button(f1, text = SKIP_TEXT[2], command = lambda:self.skip(SKIP_ARRAY[2]))
        self.skip_buttons[3] = tk.Button(f1, text = SKIP_TEXT[3], command = lambda:self.skip(SKIP_ARRAY[3]))
        self.skip_buttons[4] = tk.Button(f1, text = SKIP_TEXT[4], command = lambda:self.skip(SKIP_ARRAY[4]))
        self.skip_buttons[5] = tk.Button(f1, text = SKIP_TEXT[5], command = lambda:self.skip(SKIP_ARRAY[5]))
        self.skip_buttons[6] = tk.Button(f1, text = SKIP_TEXT[6], command = lambda:self.skip(SKIP_ARRAY[6]))
        self.skip_buttons[7] = tk.Button(f1, text = SKIP_TEXT[7], command = lambda:self.skip(SKIP_ARRAY[7]))
        self.skip_buttons[8] = tk.Button(f1, text = SKIP_TEXT[8], command = lambda:self.skip(SKIP_ARRAY[8]))
        self.skip_buttons[9] = tk.Button(f1, text = SKIP_TEXT[9], command = lambda:self.skip(SKIP_ARRAY[9]))
        self.skip_buttons[10] = tk.Button(f1, text = SKIP_TEXT[10], command = lambda:self.skip(SKIP_ARRAY[10]))
        self.skip_buttons[11] = tk.Button(f1, text = SKIP_TEXT[11], command = lambda:self.skip(SKIP_ARRAY[11]))
        self.end_button = tk.Button(f1, text = u"→", command = lambda:self.skip(self.win.videolength() - self.win.getframe()))

        self.start_button.pack(side = tk.LEFT)
        for i in self.skip_buttons:
            i.pack(side = tk.LEFT)
        self.end_button.pack()
        # for l in zip(SKIP_ARRAY, SKIP_TEXT):
        #     self.skip_buttons.append(tk.Button(f1,text = l[1], command = lambda:self.skip(l[0])))
        #     self.skip_buttons[len(self.skip_buttons) - 1].pack(side = tk.LEFT)
        f1.pack()

        f2 = tk.Frame(self)
        self.position_label1 = tk.Label(f2, text = "frame count:")
        self.position_label2 = tk.Label(f2)
        self.position_label3 = tk.Label(f2, text = " / ")
        self.position_label4 = tk.Label(f2)
        self.position_label1.pack(side = tk.LEFT)
        self.position_label2.pack(side = tk.LEFT)
        self.position_label3.pack(side = tk.LEFT)
        self.position_label4.pack(side = tk.LEFT)
        f2.pack()

    def skip(self, l):
        frame_number = self.win.getframe()
        frame_number += l
        self.win.setframe(frame_number)
        self.win.showframe()
        self.position_label2.config(text = str(self.win.getframe()))

    def choose_movie(self):
        self.movie_filename = filedialog.askopenfilename()
        print(self.movie_filename)
        self.cm_button.configure(text = self.movie_filename)
        self.win = Playwindow(self.movie_filename)
        self.position_label4.configure(text = str(self.win.videolength()))
        self.skip(0)

class Playwindow:
    def __init__(self, movie_filename):
        self.size = SIZE
        self.frame_number = 0
        self.cap = cv2.VideoCapture(movie_filename)
        self.length = self.decide_length()
        if self.cap.isOpened() != True:
            print("file not found")

    def decide_length(self):
        candidate = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, candidate)
            if self.cap.grab():
                return candidate
            candidate -= 1

    def getframe(self):
        return self.frame_number

    def setframe(self, frame_number):
        self.frame_number = frame_number
        print(self.frame_number)

    def videolength(self):
        return self.length

    def showframe(self):
        if self.frame_number > self.length:
            self.frame_number = self.length
        elif self.frame_number < 0:
            self.frame_number = 0

        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
        ret, frame = self.cap.read()
        print(ret)

        cv2.imshow("show window", self.resize(frame))
        cv2.waitKey(60)

    def resize(self, frame):
        return cv2.resize(frame, self.size)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
