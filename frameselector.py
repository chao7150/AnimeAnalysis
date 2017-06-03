import cv2
import tkinter as tk
from tkinter import filedialog

#フレームジャンプ幅の既定値
SKIP_ARRAY = [-100, -50, -10, -5, -1, 1, 5, 10, 50, 100]
#画面サイズ（16:9）
SIZE = (480, 270)

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    #GUI作る
    def create_widgets(self):
        #GUIの1行目
        f1 = tk.Frame(self)
        #動画ファイル読み込みボタン
        self.choose_button = tk.Button(f1, text = "choose movie file", command = self.load_movie)
        self.choose_button.pack()
        f1.pack()

        #GUIの2行目
        f2 = tk.Frame(self)
        #1フレーム目ジャンプボタン
        self.start_button = tk.Button(f2, text = u"←", command = lambda: self.jump(0))
        #最終フレームジャンプボタン
        self.end_button   = tk.Button(f2, text = u"→", command = lambda: self.jump(self.length))
        self.start_button.pack(side = tk.LEFT)
        #現在のフレームから一定フレームジャンプするボタン
        self.skip_buttons = []
        for i in SKIP_ARRAY:
            self.skip_buttons.append(tk.Button(f2, text = str(i), command = self.button_cmd(i)))
            self.skip_buttons[-1].pack(side = tk.LEFT)
        self.end_button.pack(side = tk.LEFT)
        f2.pack()

        #GUIの3行目
        f3 = tk.Frame(self)
        #4つのラベルで"frame count X / Y"という形式を作る
        self.position_label1  = tk.Label(f3, text = "frame count")
        self.currentpos_label = tk.Label(f3)
        self.position_label2  = tk.Label(f3, text = " / ")
        self.max_label        = tk.Label(f3)
        self.position_label1.pack(side = tk.LEFT)
        self.currentpos_label.pack(side = tk.LEFT)
        self.position_label2.pack(side = tk.LEFT)
        self.max_label.pack(side = tk.LEFT)
        f3.pack()

    #同じコールバック関数の引数を変えて使いまわすときなぜかこうしないとうまくいかない
    def button_cmd(self, i):
        def nest():
            self.move(i)
        return nest

    def load_movie(self):
        #ダイアログから動画ファイルを選択
        self.movie_filename = filedialog.askopenfilename()
        #読み込みが成功した場合
        if self.movie_filename:
            #ボタンに読み込んだファイル名を載せる
            self.choose_button.configure(text = self.movie_filename)
            #openCVで動画を読み込む
            self.cap = cv2.VideoCapture(self.movie_filename)
            #openCVの総フレーム数取得は間違うので正確な総フレーム数を求める
            self.length = self.precise_length()
            #取得した総フレーム数をラベルに載せる
            self.max_label.configure(text = str(self.length))
            #デフォルト位置は動画冒頭
            self.frame_number = 0
            #画面を映す
            self.showframe()

    #正確な総フレーム数を求めるための関数
    def precise_length(self):
        #cap.getで得られる総フレーム数は実際よりも数フレーム多い
        candidate = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        #cap.getで得られたフレームを1ずつ減らしながら読み込める一番後ろのフレームを探す
        while True:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, candidate)
            if self.cap.grab():
                return candidate
            candidate -= 1

    #現在位置のフレームを動画から読み出し画面に表示する
    def showframe(self):
        #読めないフレームを読もうとしないように条件分岐
        if self.frame_number > self.length:
            self.frame_number = self.length
        elif self.frame_number < 0:
            self.frame_number = 0

        #読むべきフレームをcapに教える
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_number)
        #フレームを読み出す
        ret, frame = self.cap.read()
        #何フレーム目を読み出しているかラベルに表示する
        self.currentpos_label.configure(text = str(self.frame_number))
        #読み出したフレームをリサイズして画面に表示する
        cv2.imshow("show window", self.resize(frame))

    #リサイズ
    def resize(self, frame):
        return cv2.resize(frame, SIZE)

    #フレームの絶対位置を指定して移動し表示する
    def jump(self, dest):
        self.frame_number = dest
        self.showframe()

    #フレームの相対位置を指定して移動し表示する
    def move(self, step):
        self.frame_number += step
        self.showframe()

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
