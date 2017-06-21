#基本的なアイデアは　http://kivantium.hateblo.jp/entry/2015/02/02/203209　からお借りしました

import numpy as np
import cv2
import sys
import start
import gc

filename, START, END = start.start()
print(filename)
#ビデオ読み込み
cap = cv2.VideoCapture(filename)
if cap.isOpened() != True:
    print("load failed")
    sys.exit()

images = []
frame_number = START
cap.set(cv2.CAP_PROP_POS_FRAMES, START)

#動画の最初からFRAME番目のフレームまでをキャプチャしimages配列に入れる
while cap.isOpened() and frame_number <= END:
    ret, image = cap.read()
    images.append(cv2.resize(image,None, fx = 0.5, fy = 0.5))
    frame_number += 1

#キャプチャした画像のサイズとカラーチャンネル数を取得
shape = images[0].shape
print(shape)

#取り出した画像のリストをnumpy.arrayに変換
images_a = np.asarray(images)

#最頻値を計算
imgvar = np.var(images_a, axis=0)
imgmask = abs(imgvar) < 25
images[0][imgmask] = 0

#出来上がった画像を保存
cv2.imwrite("filename"+"_bg_"+str(START)+"-"+str(END)+".png", np.asarray(images[0]))
